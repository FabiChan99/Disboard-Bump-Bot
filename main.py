import discord
from discord.ext import commands
from datetime import datetime
import json
import asyncio

TOKEN = "BOT TOKEN HERE"

INTENTS = discord.Intents.all()
bot = commands.Bot(command_prefix="agcbump", intents=INTENTS)

CHANNELID = 000000000000000 #Channel ID Here
SERVERID = 000000000000000 #Server ID Here



@bot.event
async def on_message(message):
    if message.author.id == 302050872383242240: #bump bot ID
        if ':thumbsup:' in message.embeds[0].description:
            with open(r'data/bumptime.json', 'r') as file:
                timedata = json.load(file)
            timedata["lastbump"] = str(datetime.utcnow())
            with open(r'data/bumptime.json', 'w') as file:
                json.dump(timedata, file, indent=4)


async def bump_check():
    await bot.wait_until_ready()
    while True:
        with open(r'data/bumptime.json', 'r') as f:
            cache = json.load(f)
        data = cache["lastbump"]
        if not data == str(0):
            last_bumped = datetime.strptime(data, '%Y-%m-%d %H:%M:%S.%f')
            now = datetime.utcnow()
            diff = now - last_bumped
            time_data = int(diff.total_seconds())
            if time_data > 7200:
                cache["lastbump"] = str(0)
                with open(r'data/bumptime.json', 'w') as f:
                    json.dump(cache, f, indent=4)
                channel = bot.get_channel(CHANNELID)
                embed = discord.Embed(title="This Server can bumped again!", description=f"Type ```!d bump``` to bump at https://disboard.org/de/server/{SERVERID}/", color=discord.Color.blurple())
                await channel.send(content="<@&904455037344968705>", embed=embed)
        await asyncio.sleep(60)

@bot.event
async def on_ready():
    print("Started")
    bot.loop.create_task(await bump_check())

bot.run(TOKEN)
