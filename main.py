# Written by Felipe Galindo & GoldyDog himself
# Version 7.0.0

# Main.py 
# For GoldyChat, a Powerful Open Source ChatGPT Chatbot. It can communicate with users via Discord, Terminal, and more.

# TODO UPDATE THIS FILE so that it launches puppeteer right after the "await Init_Systems()" line is executed. As a test open OpenAI's website and see if it works. If it does, then we can start working on the chatbot itself.

# Imports
import discord
import threading
import asyncio

from config import BOT_TOKEN
from Discord import client, send_discord_message_with_image
import subprocess

from UserTerminal import handle_terminal_input  # Import the function that runs the terminal
from text_colors import Colors, print_colors  # Import the text colors
from Init import Init_Systems, Init_Memory_Systems, Init_NLPM, Init_NLCM, Init_Feedback_Algorithm, Init_IGN, Init_CGM, Init_Chatbot, Init_Discord_Client  # Import the init functions

#print(f"Bot token: {BOT_TOKEN}")

chatbot_version = "7.0.0"
chatbot_name = "GoldyChatAI"




async def startGoldyChatAI():
    print_colors()

    print(F"\n\n\n{Colors.GREEN}Starting {chatbot_name} {chatbot_version}...{Colors.RESET}")
    
    await Init_Systems()

    # Start listening for terminal input
    asyncio.create_task(handle_terminal_input())

    # Run the discord client in the same event loop
    await client.start(BOT_TOKEN)

# Start the bot
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(startGoldyChatAI())





