# HybridPuppeteer.py is a script that uses Puppeteer to take screenshots of webpages and sends them to a Discord channel.

import requests
import asyncio
import subprocess
import os
import discord
import threading
import asyncio
import subprocess


from Discord import client, send_discord_message_with_image


from text_colors import Colors, print_colors  # Import the text colors

Channel_ID = 1109599781686349874
server_url = "http://localhost:3000/"
screenshot_directory = '/home/goldyosv7/GoldyChat/WebScreenshots'  # Specify the directory to save the screenshots

loop = asyncio.get_event_loop()

def start_server():
    print(f"{Colors.YELLOW}@start_server{Colors.RESET}")
    subprocess.Popen(['node', 'GoldyChat/server.js'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"{Colors.GREEN}Server started{Colors.RESET}")

async def start_browser():
    command = f'{server_url}start'

    print(f"{Colors.YELLOW}@start_browser: {command}{Colors.RESET}")

    await asyncio.sleep(5) # Wait for the server to start

    try:
        requests.get(command)
    except Exception as e:
        print(f"Failed to start browser: {e}")
    
    print(f"{Colors.GREEN}Browser started ✅{Colors.RESET}")


def open_url(url):
    command = f'{server_url}openURL?url={url}'
    print(f"{Colors.YELLOW}@open_url: {command}{Colors.RESET}")
    response = requests.get(command)
    page_id = response.json()['pageId']
    print(f"{Colors.GREEN}Opened URL: {url} ✅{Colors.RESET}")
    return page_id

def take_screenshot(page_id):
    command = f'{server_url}takeScreenshot?pageId={page_id}'
    print(f"{Colors.YELLOW}@take_screenshot: {command}{Colors.RESET}")
    response = requests.get(command)
    screenshot_path = response.json()['screenshotPath']
    print(f"{Colors.GREEN}Took screenshot for pageId: {page_id} ✅{Colors.RESET}")
    return screenshot_path

def close_tab(page_id):
    command = f'{server_url}closeTab?pageId={page_id}'
    print(f"{Colors.YELLOW}@close_tab: {command}{Colors.RESET}")
    requests.get(command)
    print(f"{Colors.GREEN}Closed tab for pageId: {page_id} ✅{Colors.RESET}")

def screenshot(url):
    command = f'{server_url}screenshot?url={url}'
    print(f"{Colors.YELLOW}@screenshot: {command}{Colors.RESET}")
    response = requests.get(command)
    screenshot_path = response.json()['screenshotPath']
    print(f"{Colors.GREEN}Screenshot taken ✅{Colors.RESET}")
    return screenshot_path


# async def test_hybrid_Puppeteer():
#     print(f"{Colors.YELLOW}@test_hybrid_Puppeteer{Colors.RESET}")
#     # Call the Puppeteer script
#     print("Running Puppeteer script...")
#     start_server()
#     await start_browser()
#     print("Puppeteer Browser Startup Completed ✅")
    
#     # Send each screenshot to the Discord channel
#     urls = ['https://chat.openai.com', 'https://www.google.com', 'https://github.com/UMN-VR/GoldyDogV7']
#     for url in urls:
#         page_id = await loop.run_in_executor(None, open_url, url)
#         screenshot_path = await loop.run_in_executor(None, take_screenshot, page_id)
#         await loop.run_in_executor(None, close_tab, page_id)
#         message = "Here's a screenshot"
#         print(f"Sending screenshot: {screenshot_path}")
#         await send_discord_message_with_image(message, screenshot_path, Channel_ID)
#         print(f"Sent screenshot: {screenshot_path}")

#     print("All screenshots sent to Discord.")


async def test_hybrid_Puppeteer():
    print(f"{Colors.YELLOW}@test_hybrid_Puppeteer{Colors.RESET}")
    # Call the Puppeteer script
    print("Running Puppeteer script...")
    start_server()
    await start_browser()
    print("Puppeteer Browser Startup Completed ✅")
    
   
    # Send each screenshot to the Discord channel
    urls = ['https://chat.openai.com', 'https://www.google.com', 'https://github.com/UMN-VR/GoldyDogV7']
    for url in urls:
        page_id = await loop.run_in_executor(None, open_url, url)
        screenshot_path = await loop.run_in_executor(None, take_screenshot, page_id)
        await loop.run_in_executor(None, close_tab, page_id)
        message = "Here's a screenshot"
        print(f"Sending screenshot: {screenshot_path}")
        await send_discord_message_with_image(message, screenshot_path, Channel_ID)
        print(f"Sent screenshot: {screenshot_path}")

    print("All screenshots sent to Discord.")
