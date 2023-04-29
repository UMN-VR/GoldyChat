import discord
import openai
import threading
from config import BOT_TOKEN

from Discord import handle_message

#print(f"Bot token from config: {BOT_TOKEN}")

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
    "fact1": "Your responses are analyzed and you can communicate with people through Discord or voice recognition and synthesis.",
    "info_about_you0": "Understand that people may refer to you as GoldyDog or GoldyChat. ",
    "info_about_you1": "You have a speaker, microphone, camera, and an internet connection.",
    "info_about_you2": "Your purpose is to help and engage in conversations with users and be entertaining.",
    "earlier_info0": "You are a Robot Dog"
}

def handle_terminal_input():
    while True:
        user_input = input()
        if user_input == "PRINT_KNOWLEDGE":
            print("\nKnowledge log:")
            for key, value in knowledge_log.items():
                print(f"{key}: {value}")
            print()

# Event listener for when the bot is ready
@client.event
async def on_ready():
    print(f'\nLogged in as {client.user}')
    print("Ready for input \n")
    # Start a separate thread to handle terminal input
    terminal_thread = threading.Thread(target=handle_terminal_input)
    terminal_thread.daemon = True
    terminal_thread.start()

# Event listener for when a message is received
@client.event
async def on_message(message):
    print(f"Got message:{message}")
    await handle_message(message, conversation_log, knowledge_log)

# Start the bot
client.run(BOT_TOKEN)
