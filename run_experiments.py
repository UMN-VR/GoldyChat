# run_experiments.py this file contains a function called run_experiments() that will run the puppeteer script and send the screenshots to the Discord channel. 
# When the code is mode developed it will be moved to its own file.

#TODO update this file to use the new pupeeteer script
# Imports
import requests
import os
import discord
import threading
import asyncio
import subprocess

from config import BOT_TOKEN
from Discord import client, send_discord_message_with_image


from text_colors import Colors, print_colors  # Import the text colors
from HybridPuppeteer import start_server, start_browser, screenshot
from HybridPuppeteer import test_hybrid_Puppeteer

Channel_ID = 1109599781686349874
screenshot_directory = '/home/goldyosv7/GoldyChat/WebScreenshots'  # Specify the directory to save the screenshots







async def run_experiments():
    print(f"{Colors.YELLOW}@run_experiments")

    await test_hybrid_Puppeteer()

   
    print("Experiments completed.")