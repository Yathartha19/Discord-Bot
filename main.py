import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
import datetime
import pytz

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
TARGET_CHANNEL_ID = int(os.getenv('TARGET_CHANNEL_ID'))

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)  

TIMEZONE = pytz.timezone('Asia/Kolkata') 

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    good_morning.start()

@tasks.loop(minutes=1)
async def good_morning():
    now = datetime.datetime.now(TIMEZONE)
    channel = bot.get_channel(TARGET_CHANNEL_ID)
    if channel:
        if now.hour == 10 and now.minute == 52:
            await channel.send("☀️ Good morning, everyone! Have an amazing day ahead!")
        elif now.hour == 22 and now.minute == 0:
            await channel.send("🌙 Good night, everyone! Sleep well!")
        else:
            pass  
    else:
        print("Channel not found!")

bot.run(TOKEN)
