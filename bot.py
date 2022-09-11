import random
import discord
import httpx
import time
import config
import hashlib
import os
from discord.ext import commands

if not os.path.exists("cats"):
    os.mkdir("cats")

client = httpx.AsyncClient()

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

last_request=0

async def get_cat():

    global last_request
    t = time.time()
    if t - last_request > 10:
        print("renew cache")
        r = await client.get("https://cataas.com/cat/gif")
        r.raise_for_status()
        pic_hash = f"{hashlib.sha256(r.content).hexdigest()}.gif"
        with open(f"cats/{pic_hash}", "wb") as f:
            f.write(r.content)
        last_request = t
    else:
        print("use old cache")
        pic_hash = random.choice(os.listdir("cats"))
    return f"cats/{pic_hash}"


    last_request = time.time()
    
    return f"cats/{pic_hash}.gif"



@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}") 



#@bot.event
#async def on_message(message: discord.Message, ctx):
#    if message.content.startswith("!cat"):
#        await ctx.send(file=discord.File(await get_cat()))

@bot.command()
async def cat(ctx):
    await ctx.send(file=discord.File(await get_cat()))


bot.run(config.TOKEN)