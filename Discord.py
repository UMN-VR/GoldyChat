import discord

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
    print(f"\nFinal Discord Text Sent: '{message}'\n")
    await channel.send(message)
