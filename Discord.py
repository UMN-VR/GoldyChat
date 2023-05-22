# Discord.py file
import discord
from text_colors import Colors


# Define the intents for the bot
intents = discord.Intents.all()
intents.members = True

# Create the client object with the specified intents
client = discord.Client(intents=intents)

async def send_discord_message_with_image(message, image_path, channel_ID):
    channel = client.get_channel(channel_ID)
    if channel is None:
        print(f"Couldn't find a channel with the id {channel_ID}")
    else:
        # Create a File object from the image path
        file = discord.File(image_path, filename=image_path)
        # Send the file
        await channel.send(message, file=file)

async def send_discord_message_channel_ID(message, predefined_channel):
    print(f"\n{Colors.BRIGHT_MAGENTA}Final Discord Text Sent to {predefined_channel}: '{message}'\n{Colors.RESET}")
    channel = client.get_channel(predefined_channel)
    if channel is None:
        print(f"Couldn't find a channel with the id {predefined_channel}")
    else:
        await channel.send(message)



async def send_discord_message(message, channel):
    for word in message.split():
        if word.startswith("@"):
            username = word[1:]
            if username.lower() == "clyde":
                message = message.replace(word, "<@!473606944708493324>")
                print(f"Replaced {word} with <@!473606944708493324>")
            else:
                member = discord.utils.get(channel.guild.members, name=username)
                if member:
                    message = message.replace(word, f"<@!{member.id}>")
                    print(f"Replaced {word} with <@!{member.id}>")
                else:
                    print(f"No member found with name {username}")
    print(f"\n{Colors.BRIGHT_MAGENTA}Final Discord Text Sent: '{message}'\n{Colors.RESET}")
    await channel.send(message)



