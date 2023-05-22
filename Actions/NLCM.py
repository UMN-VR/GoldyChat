# NLCM.py
from text_colors import Colors
import asyncio
from Discord import send_discord_message_channel_ID

NLCM_channel = 1109211766841430086

def Init_NLCM():
    print(F"{Colors.WHITE}Init NLCM(Natural Language Consciousness Simulator Module)... {Colors.RESET}", end='')

    result = "OK"
    print(F"{Colors.GREEN}{result}{Colors.RESET}")

async def run_NLCM():
    print(F"{Colors.RESET}@run_NLCM{Colors.RESET}")
    await send_discord_message_channel_ID("NLCM is running.", NLCM_channel)
    await asyncio.sleep(10)
    result = "OK"
    print(F"{Colors.RESET}@run_NLCM result: {Colors.GREEN}{result}{Colors.RESET}")

