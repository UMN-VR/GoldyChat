import discord
import asyncio

from config import BOT_TOKEN
from Bot import handle_message
from knowledge_log import global_knowledge_log
from Discord import send_discord_message

client = discord.Client()

# The channel where the bot will respond to messages from the terminal
TERMINAL_CHANNEL_ID = 1234567890

# The event loop used by the terminal
loop = asyncio.get_event_loop()


async def handle_terminal_input(terminal_channel):
    while True:
        user_input = input("> ")
        if user_input == "EXIT":
            await terminal_channel.send("Exiting terminal mode...")
            await asyncio.sleep(1)
            await loop.shutdown_asyncgens()
            await loop.stop()
        elif user_input.startswith("SEND"):
            _, message_content = user_input.split(maxsplit=1)
            # Generate a response using the bot's conversation log and knowledge log
            response = await handle_message("Terminal", "Terminal", message_content, [], global_knowledge_log, {})
            # Send the response to the terminal channel
            await send_discord_message(response, terminal_channel)
        elif user_input == "PRINT_KNOWLEDGE":
            print("\nGlobal knowledge log:")
            for key, value in global_knowledge_log.items():
                print(f"{key}: {value}")
            print()
        else:
            print("Invalid command.")


@client.event
async def on_ready():
    print(f'Logged in as {client.user} in terminal mode.')
    print(f'Send messages to the bot using the "SEND" command.')
    print(f'Type "EXIT" to exit the terminal.\n')

    # Get the terminal channel object
    terminal_channel = client.get_channel(TERMINAL_CHANNEL_ID)

    # Start listening to user input from the terminal
    await handle_terminal_input(terminal_channel)


if __name__ == '__main__':
    client.run(BOT_TOKEN, bot=False)
    loop.run_until_complete(client.logout())
    loop.close()
