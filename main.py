import discord
import openai
import random

import config

import prompts
import helpers

openai.api_key = config.API_KEY
TOKEN = config.BOT_TOKEN

# Initialize an empty conversation log
conversation_log = []

# Define the intents for the bot
intents = discord.Intents.all()
intents.members = True
# Create the client object with the specified intents
client = discord.Client(intents=intents)

# Event listener for when the bot is ready
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    print("Ready for input")

# Event listener for when a message is received
@client.event
async def on_message(message):
    print(f"Got message:{message}")
    await helpers.handle_message(message, conversation_log, client)

# Start the bot
client.run(TOKEN)
