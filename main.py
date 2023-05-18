# Main.py for GoldyChat a Open Source ChatGPT Discord Chatbot
import discord
import threading

from actions import predefined_responses
from Bot import handle_message
from config import BOT_TOKEN
from knowledge_log import global_knowledge_log

#print(f"Bot token: {BOT_TOKEN}")

# Define the intents for the bot
intents = discord.Intents.all()
intents.members = True

# Create the client object with the specified intents
client = discord.Client(intents=intents)

# Init memory
channel_memory = {}

# Initialize an empty conversation log
conversation_log = []


# Event listener for when the bot is ready
@client.event
async def on_ready():
    print(f'\nLogged in as {client.user}')
    print("Ready for input \n")
    # Start a separate thread to handle terminal input
    terminal_thread = threading.Thread(target=run_user_terminal, args=(client,))
    terminal_thread.daemon = True
    terminal_thread.start()

# Event listener for when a message is received
@client.event
async def on_message(message):
    
    print(f"Got message:{message}")

    # Ignore messages from the bot itself
    if message.author.bot:
        return
    
    # Get the channel id
    channel_id = message.channel.id
    
    # Initialize user memory if it does not exist
    if channel_id not in channel_memory:
        channel_memory[channel_id] = {
            'conversation_log': []
        }
    
    # Get the conversation log for the channel
    channel_conversation_log = channel_memory[channel_id]['conversation_log']

    # Get server and channel name
    server_name = message.guild.name
    channel = message.channel

    print(f"\nMessage from {message.author} in server '{server_name}' and channel '#{channel}': {message.content}")

    await handle_message(server_name, channel, message, channel_conversation_log, global_knowledge_log, predefined_responses)

# Start the bot
if __name__ == '__main__':
    client.run(BOT_TOKEN)
