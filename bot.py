import os
import discord
import requests
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

intents = discord.Intents.default()
intents.members = True
intents.guilds = True

client = discord.Client(intents=intents)

def send_to_telegram(username, user_id, guild_name, is_bot=False):
    """Send new member notification to Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    bot_tag = " [BOT]" if is_bot else ""
    message = (
        f"🎉 New member joined {guild_name}!\n\n"
        f"👤 Username: {username}{bot_tag}\n"
        f"🆔 ID: {user_id}"
    )
    
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    
    try:
        response = requests.post(url, data=payload, timeout=10)
        print(f"✅ Telegram message sent for {username}")
    except Exception as e:
        print(f"❌ Error sending to Telegram: {e}")

@client.event
async def on_ready():
    print(f"✅ Bot logged in as {client.user}")
    print(f"📊 Monitoring {len(client.guilds)} server(s)")
    for guild in client.guilds:
        print(f"   - {guild.name} (Owner: {guild.owner})")

@client.event
async def on_member_join(member):
    """Triggered when any new member joins ANY server the bot is in"""
    guild = member.guild
    username = member.name
    user_id = member.id
    is_bot = member.bot
    
    print(f"✅ New member: {username} joined {guild.name}")
    
    # Send to Telegram for every member join (including bots)
    send_to_telegram(username, user_id, guild.name, is_bot)

client.run(DISCORD_TOKEN)
