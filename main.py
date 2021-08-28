from replit import db
import os
import discord
import requests
import json
import random
from keep_alive import keep_alive
import praw
from prawcore import NotFound

my_secret = os.environ['TOKEN']
clientIDPraw = os.environ['CLIENTID']
clientSecretPraw = os.environ['CLIENTSECRET']

default_subreddits = ["okbuddyretard", "dankmemes","wholesomememes","me_irl", "2meirl4meirl", "ape","crackheadcraigslist","depression_memes", "memes", "hmmm", "holup", "monke", "adviceanimals", "terriblefacebookmemes","funny"]

reddit = praw.Reddit(client_id= clientIDPraw,
                            client_secret=clientSecretPraw,
                            user_agent="Discord Meme Bot",
)

client = discord.Client()

@client.event
async def on_ready():
    print("We have logged in as " + str(client.user))


@client.event
async def on_message(msg):
    #if it is the bot sending a message, do nothing
    if msg.author == client.user:
        return

    if msg.content.startswith("-meme"):
        #if alguma coisa depois de meme, -meme dankmemes, procura nesse subreddit
        try:
          specificSub = msg.content.split("-meme ", 1)[1]
          if(specificSub != None):
            exists = True
            try:
              reddit.subreddits.search_by_name(specificSub, exact=True)
            except NotFound:
              exists = False
        
          if (exists == True): #if subreddit exists
                meme = get_specific_meme(specificSub)
                await msg.channel.send("From r/" + meme['subreddit'])
                await msg.channel.send(meme['title'])
                await msg.channel.send(meme['url'])
                return
          else:
            await msg.channel.send("Subreddit doesn't exist :(")

        except:
          pass
        meme = get_meme()
        await msg.channel.send("From r/" + meme['subreddit'])
        await msg.channel.send(meme['title'])
        await msg.channel.send(meme['url'])


    elif msg.content.startswith("-add"): #-add memes, add subreddit
        print(msg.content.split("-add ", 1)[1]) #subreddit name

        sub2add = msg.content.split("-add ", 1)[1]
        #remove spaces from subreddit
        
        exists = True
        try:
          reddit.subreddits.search_by_name(sub2add, exact=True)
        except NotFound:
          exists = False
        
        if (exists == True):
          if (add_subreddit(sub2add) == 1):
            subredditsNow = db["subreddits"]
            await msg.channel.send("Current subreddits => "+ str(list(subredditsNow)))
          else:
            await msg.channel.send("Subreddit already being used :)")
        else:
          await msg.channel.send("Subreddit doesn't exist :(")
    
    elif msg.content.startswith("-remove"): #-remove dankmemes, remove subreddit
        print(msg.content.split("-remove ", 1)[1])
        #if valid subreddit
        #    add to database
        
        subredditsNow = []
        if "subreddits" in db.keys(): #If there are already subreddits in the db
          sub2remove = msg.content.split("-remove ", 1)[1]
          #remove spaces from subreddit
          remove_subreddit(sub2remove)
          subredditsNow = db["subreddits"]
        await msg.channel.send("Current subreddits => "+ str(list(subredditsNow)))
    
    elif msg.content.startswith("-list"): # list all subreddits
        print(msg)
        subredditsNow = db["subreddits"]
        await msg.channel.send("Current subreddits => "+ str(list(subredditsNow)))

    elif msg.content.startswith("-help"): # list all commands
        print(msg)
        await msg.channel.send("The available commands are: ")
        await msg.channel.send("```-meme => To get a random meme from the saved subreddits\n-meme subreddit => To get a meme from the specified subreddit\n-add subreddit => To add a subreddit to the database to look for memes\n-remove subreddit => To remove a subreddit from the database to look for memes\n-drop => To drop the subreddits from the database and set to the default ones\n-list => To list all of the subreddits in the database```")
        

    elif msg.content.startswith("-drop"): # drop subreddits to default
        print(msg)
        db["subreddits"] = default_subreddits
        print (db["subreddits"])
        await msg.channel.send("Subreddits set to default!")



def get_meme():
    #multiple subreddits, add yours
    #Fazer comando para adicionar subreddits a database e adiciona los
    #a lista para escolher
    #ou retirar da database e usa los
    #-meme subreddit
    options = []
    if "subreddits" in db.keys():
      options = db["subreddits"]
    random_sub = random.choice(options)
    response = requests.get("https://meme-api.herokuapp.com/gimme/" + random_sub)
    json_data = json.loads(response.text)
    return json_data

def get_specific_meme(sub):
    #multiple subreddits, add yours
    #Fazer comando para adicionar subreddits a database e adiciona los
    #a lista para escolher
    #ou retirar da database e usa los
    #-meme subreddit
    response = requests.get("https://meme-api.herokuapp.com/gimme/" + sub)
    json_data = json.loads(response.text)
    return json_data

#Store subreddits in the database => key,value
def add_subreddit(new_subreddit):
  if "subreddits" in db.keys(): #if key already exists
    if new_subreddit not in db["subreddits"]:
      subs = db["subreddits"]
      subs.append(new_subreddit)
      db["subreddits"] = subs
      return 1
    else:
      return -1
  else: #if key doesnt exist
    db["subreddits"] = [new_subreddit]
    return 1

def remove_subreddit(subreddit_to_remove):
  subreddits = db["subreddits"]
  if subreddit_to_remove in subreddits:
    #delete from database if it exists
    del subreddits[subreddits.index(subreddit_to_remove)]
    db["subreddits"] = subreddits
    print(db["subreddits"])
  else:
    pass
    #do nothing
    

keep_alive()
client.run(my_secret)
