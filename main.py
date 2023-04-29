import discord
import openai
import config

from Discord import handle_message


openai.api_key = config.API_KEY
TOKEN = config.BOT_TOKEN
# Define the intents for the bot
intents = discord.Intents.all()
intents.members = True
# Create the client object with the specified intents
client = discord.Client(intents=intents)
# Initialize an empty conversation log
conversation_log = []
# Initialize an empty knowledge log
knowledge_log = {
    "fact0": "You are GoldyChat, a ChatGPT-4 powered AI chatbot that lives inside a quadruped robotic dog called GoldyDog.",
    "info_about_you0": "Understand that people may refer to you as GoldyDog or GoldyChat. You have a speaker, microphone, and an internet connection.",
    "info_about_you1" : "Your responses are analyzed and you can communicate with people through Discord or voice recognition and synthesis. Your purpose is to help and engage in conversations with users and be entertaining.",
    "earlier_info0": ""
}
# Event listener for when the bot is ready
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    print("Ready for input \n")
# Event listener for when a message is received
@client.event
async def on_message(message):
    print(f"Got message:{message} ")
    await handle_message(message, conversation_log, knowledge_log)

# Start the bot
client.run(TOKEN)
