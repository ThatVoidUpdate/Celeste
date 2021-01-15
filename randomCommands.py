import discord

import config

commands = {
    "mine":{"name": "Mine", "description": "Mines for minerals and ores"},
    "hello":{"name": "Hello", "description": "A test command. Simply replies Hello"},
    "help":{"name": "Help", "description": "Show all the commands and how to use them"}
}


async def Hello(message: discord.Message) -> None:
    await message.channel.send("Hello!")

async def Help(message: discord.Message) -> None:
    embed = discord.Embed(title=f"Help", description=f"")
    for command in commands:
        embed.add_field(name=f"{commands[command]['name']} - `{config.CommandPrefix}{command}`", value=f"{commands[command]['description']}", inline=False)

    await message.channel.send(embed=embed)