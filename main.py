import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
import datetime
import pytz

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

TIMEZONE = pytz.timezone('Asia/Kolkata')

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands.")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

    good_morning.start()

async def get_general_channels():
    """
    Looks for 'general' channel in every server the bot is in.
    Returns a list of all found channels.
    """
    general_channels = []
    for guild in bot.guilds:
        for channel in guild.text_channels:
            if channel.name == "general":
                general_channels.append(channel)
                break  
    return general_channels

@tasks.loop(minutes=1)
async def good_morning():
    now = datetime.datetime.now(TIMEZONE)
    channels = await get_general_channels()
    if channels:
        for channel in channels:
            if now.hour == 7 and now.minute == 0:
                await channel.send("☀️ Good morning, everyone! Have an amazing day ahead!")
            elif now.hour == 22 and now.minute == 0:
                await channel.send("🌙 Good night, everyone! Sleep well!")
    else:
        print("No general channels found!")

@bot.tree.command(name="ping", description="Ping to keep Active Developer Badge")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("🏓 Pong!")

bot.run(TOKEN)
