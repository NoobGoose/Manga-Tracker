from keep_alive import keep_alive
import requests
import discord
import asyncio
import ast

client = discord.Client()

async def update_runner():
    await client.wait_until_ready()
    while not client.is_closed():
      channel_id = open("channel_id.txt")
      channel_id = channel_id.read()
      channel = client.get_channel(id=int(channel_id))
      print("update()")
      delete_val = update()
      updated = check_for_update()
      if updated != [] and delete_val:
        print(updated)
        await channel.send(str(updated) + " has been updated!")
      await asyncio.sleep(600)

def check_for_update():
  history = open("history.txt", "r")
  history_text = history.readlines()
  prev = ast.literal_eval(history_text[0])
  post = ast.literal_eval(history_text[1])
  return_keys = []
  for key in prev:
    prev_val = prev[key]
    post_val = post[key]
    if prev[key].find("-") != -1:
      prev_val = prev[key][prev[key].find("-") + 1:]
    if post[key].find("-") != -1:
      post_val = val= post[key][:post[key].find("-")]
    if post_val > prev_val:
      print(key + " has been updated")
      return_keys.append(key)
  return return_keys
def update():
  url_list = open("tracking_url.txt","r")
  url_list = url_list.read()
  url_list = url_list.splitlines()
  return_dict = {}
  for url in url_list:
    page_raw = requests.get(url)
    page = page_raw.text
    page_sliced = page.splitlines()
    index = 0
    for line in page_sliced:
      if line == "<div class=\"sCat\"><b>Latest Release(s)</b></div>":
        next_line = page_sliced[index + 1]
        end_marker = next_line.find("b")
        end = end_marker - 5
        clean_line = next_line[28:end]
        return_dict[url] = clean_line

      else:
        index = index + 1

  history = open("history.txt","a+")
  history.write(str(return_dict) + "\n")
  history.close()
  history_r = open("history.txt","r")
  history_r_l = history_r.readlines()
  if len(history_r_l) > 2:
    print("Delete")
    del history_r_l[0]
    history = open("history.txt", "w+")
    for line in history_r_l:
      history.write(line)
    return True

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):

  if message.author == client.user:
      return 0

  elif message.content.startswith("/set"):
    channel_id = open("channel_id.txt","w")
    channel_id.write(str(message.channel.id))
    await message.channel.send(str(message.channel) + " has been set to track \n")

  elif message.content == "/tracking list":
    url_list = open("tracking_url.txt","r")
    await message.channel.send(url_list.read())

  elif message.content.startswith("/track"):
    url = message.content.replace("/track", "")
    url_list = open("tracking_url.txt","a+")
    url_list.write(url + "\n")
    update()
    await message.channel.send(url + " has been tracked.")


keep_alive()
client.loop.create_task(update_runner())
client.run("Token")