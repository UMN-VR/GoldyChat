# UserTerminal.py
import asyncio
import discord
import threading
from Bot import handle_message
from state import State
from Discord import send_discord_message
from text_colors import Colors
from Actions.NLCM import run_NLCM

terminal_input = None
terminal_prompt = "> "
terminal_input_lock = threading.Lock()

async def handle_terminal_input():
    global terminal_input
    while True:
        with terminal_input_lock:
            user_input = terminal_input
            terminal_input = None
        if user_input is not None:
            await process_user_input(user_input)
        else:
            await asyncio.sleep(0.1)

async def process_user_input(user_input):
    if user_input == "":
        return
    elif user_input == "EXIT":
        return
    elif user_input.startswith("SEND"):
        _, message_content = user_input.split(maxsplit=1)
        await process_message("Terminal", "Terminal", message_content, [], State.global_knowledge_log, {})
    elif user_input == "PRINT_KNOWLEDGE":
        print("\nGlobal knowledge log:")
        for key, value in State.global_knowledge_log.items():
            print(f"{key}: {value}")
        print()
    elif user_input.startswith("CHANGE_NLCM_CYCLE_TIME"):
        _, new_time = user_input.split(maxsplit=1)
        State.NLCM_cycle_time = int(new_time)
        print(f"NLCM cycle time updated to {new_time} seconds.")
    elif user_input == "PRINT_RESEARCH":
        channel_id = "Terminal"
        if channel_id in State.channel_memory:
            research_log = State.channel_memory[channel_id]['research_log']
            print("\nResearch log:")
            for entry in research_log:
                print(entry)
        else:
            print("No research log for this channel.")
    elif user_input == "PRINT_CONVERSATION":
        channel_id = State.last_channel.id
        print(f"cID: {channel_id}")

        if channel_id in State.channel_memory:
            conversation_log = State.channel_memory[channel_id]['conversation_log']
            print("\nConversation log:")
            for entry in conversation_log:
                print(entry)
        else:
            print("No conversation log for this channel.")
    elif user_input == "RUN_NLCM":
        await run_NLCM()
    else:
        print("Invalid command.")

def handle_user_input():
    global terminal_input
    while True:
        user_input = input(terminal_prompt)
        with terminal_input_lock:
            terminal_input = user_input

async def Init_terminal_IN():
    print(f"{Colors.WHITE}Init Terminal... {Colors.RESET}", end='')

    # Start the thread to handle user input
    threading.Thread(target=handle_user_input, daemon=True).start()

    # Run the coroutine in the event loop
    loop = asyncio.get_event_loop()
    loop.create_task(handle_terminal_input())

    result = "OK"
    print(f"{Colors.GREEN}{result}{Colors.RESET}")
