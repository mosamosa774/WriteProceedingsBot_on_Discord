import asyncio
import datetime
import json
import re
import os
import SummarizeDoc as sdoc

with open("token.json", "r") as f:
    data = f.read()
tokens = json.loads(data)

BOT_TOKEN = tokens['AccountToken']

import discord
client = discord.Client()

talking = {}
talked_content = {}

@client.event
async def on_ready():
    print('Logged in as')
    print('BOT-NAME :', client.user.name)
    print('BOT-ID   :', client.user.id)
    print('------')

@client.event
async def on_message(message):
    global talking
    global talked_content
    # BOTとメッセージの送り主が同じ人なら処理しない
    if client.user == message.author:
        return
    if message.content == "#talking":
        talking[message.channel.id] = True
        await client.send_message(message.channel,"start writing...")
    elif message.content == "#end":
        if message.channel.id in talking:
            if(talking[message.channel.id]):
                if(not message.channel.id in talked_content):
                    return
                del(talking[message.channel.id])
                await client.send_message(message.channel,"end writing!")
                await client.send_message(message.channel,"Dealing...")
                msg = talked_content[message.channel.id]
                del(talked_content[message.channel.id])
                summarize = sdoc.analyze(msg,5,False)
                msg += "\n\nSummarized of these proceedings\n\n"
                for i in summarize:
                    msg += i + "\n"
                with open("out.txt", mode='w') as f:
                    f.write(msg)
                await client.send_file(message.channel, "out.txt", content="done!")
    elif message.channel.id in talking:
        if(talking[message.channel.id]):
            if(not message.channel.id in talked_content):
                talked_content[message.channel.id] = ""
            talked_content[message.channel.id] += message.author.name + ": " + message.content + "\n"

client.run(BOT_TOKEN)
