import discord

import config

commands = {
    "mine":{"name": "Mine", "description": "Mines for minerals and ores"},
    "chop":{"name": "Mine", "description": "Chops down trees to get wood"},
    "smelt":{"name": "Mine", "description": "Smelts ores into ingots"},
    "hello":{"name": "Hello", "description": "A test command. Simply replies Hello"},
    "help":{"name": "Help", "description": "Show all the commands and how to use them"},
    "account":{"name": "Account", "description": "Set up an account to use with some commands"},
    "balance":{"name": "Balance", "description": "Show your current account balance"},
    "daily":{"name": "Daily", "description": "Claim your daily money reward"},
    "loot":{"name": "Loot", "description": "Search chat for any money that has been dropped"},
    "inventory":{"name": "Inventory", "description": "View your curent inventory"},
    "hug":{"name": "Hug", "description": "Hug another user. Keep adding users to make a bigger group hug"},
    "market":{"name": "Market", "description": "View the market"}
}


async def Hello(message: discord.Message) -> None:
    await message.channel.send("Hello!")

async def Help(message: discord.Message) -> None:
    embed = discord.Embed(title=f"Help", description=f"")
    for command in commands:
        embed.add_field(name=f"{commands[command]['name']} - `{config.CommandPrefix}{command}`", value=f"{commands[command]['description']}", inline=False)

    await message.channel.send(embed=embed)