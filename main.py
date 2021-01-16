import logging
import os
import sys

import discord

import creds
import config
import accountCommands
import actionCommands
import marketCommands
import moneyCommands
import randomCommands
import resourceCommands

logging.basicConfig(level=logging.INFO)

client = discord.Client()

commands = {
    "mine": resourceCommands.Mine,
    "chop": resourceCommands.Chop,
    "smelt": resourceCommands.Smelt,
    "hello": randomCommands.Hello,
    "help": randomCommands.Help,
    "account": accountCommands.CreateAccount,
    "balance": accountCommands.ViewBalance,
    "daily": moneyCommands.Daily,
    "loot": moneyCommands.Loot,
    "inventory": accountCommands.ViewInventory,
    "hug": actionCommands.Hug,
    "market": marketCommands.MarketParent,
    "giveitem": accountCommands.GiveItem
}

@client.event
async def on_ready() -> None:
    print('We have logged in as {0.user}'.format(client))

    activity = discord.Activity(name=f"{config.CommandPrefix}help", type=discord.ActivityType.playing)
    await client.change_presence(activity=activity)

@client.event
async def on_message(message: discord.Message) -> None:
    if message.author == client.user:
        return

    if message.content.startswith(config.CommandPrefix):
        await Parse(message)

@client.event
async def on_reaction_add(reaction: discord.Reaction, user: discord.Member) -> None:
    if reaction.message.author == client.user:
        print("Someone reacted to a message we sent")
        AllReactors = await reaction.users().flatten()
        #await reaction.message.channel.send(f"Thanks {' '.join([x.name for x in AllReactors])}")

async def Parse(message: discord.Message) -> None:
    print(f"Command recieved: {message.content}. Sent in channel {message.channel}")

    if message.content[len(config.CommandPrefix):].split(' ')[0] in commands:
        print("Found command in commands list, executing from there")
        await commands[message.content[len(config.CommandPrefix):].split(' ')[0]](message)
        return

    """
    Shutdown - Full shutdown of the bot
    """
    if message.content[len(config.CommandPrefix):].startswith("shutdown"):
        if message.author.id in config.AdminUsers:
            await message.channel.send('Shutting down')
            await client.logout()
        else:
            await message.channel.send('Sorry, you dont have permission to do that')

    """
    Restart - Restarts the bot
    """
    if message.content[len(config.CommandPrefix):].startswith("restart"):
        if message.author.id in config.AdminUsers:
            await message.channel.send('Restarting')
            await client.logout()
            os.startfile(sys.argv[0])
            sys.exit()
        else:
            await message.channel.send('Sorry, you dont have permission to do that')

client.run(creds.SecretKey)