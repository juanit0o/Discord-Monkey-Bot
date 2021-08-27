import os
import discord
import requests
import json
import random
from keep_alive import keep_alive

my_secret = os.environ['TOKEN']

client = discord.Client()


@client.event
async def on_ready():
    print("We have logged in as " + str(client.user))


@client.event
async def on_message(msg):
    #if it is the bot sending a message, do nothing
    if msg.author != client.user:
        return

    if msg.content.startswith("-meme"):
        meme = get_meme()
        await msg.channel.send("From r/" + meme['subreddit'])
        await msg.channel.send(meme['title'])
        await msg.channel.send(meme['url'])


def get_meme():
    #multiple subreddits, add yours
    #Fazer comando para adicionar subreddits a database e adiciona los
    #a lista para escolher
    #ou retirar da database e usa los
    subreddits = ["okbuddyretard", "dankmemes","wholesomememes","me_irl", "2meirl4meirl", "ape","crackheadcraigslist","depression_memes", "memes", "hmmm", "holup", "monke", "adviceanimals", "terriblefacebookmemes","funny"]
    random_sub = random.choice(subreddits)
    response = requests.get("https://meme-api.herokuapp.com/gimme/" + random_sub)
    json_data = json.loads(response.text)
    return json_data

keep_alive()
client.run(my_secret)
