import os
import discord
import requests
from dotenv import load_dotenv

load_dotenv()

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
RAG_API_URL = os.getenv("RAG_API_URL")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    # Ignore bot messages
    if message.author.bot:
        return

    user_input = message.content.strip()

    try:
        response = requests.post(
            RAG_API_URL,
            json={
                "question": user_input,
                "user_id": str(message.author.id)
            },
            timeout=20
        )
        data = response.json()
        answer = data.get("answer", "[Error]: No answer returned.")
        await message.channel.send(answer)

    except Exception as e:
        print(f"Error: {str(e)}")
        await message.channel.send("[Error]: Failed to contact the RAG server.")

client.run(DISCORD_BOT_TOKEN)