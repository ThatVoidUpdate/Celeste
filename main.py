import json
import logging
import os
import random
import sys
import time

import discord

import creds
import config
import accountCommands
import marketCommands
import moneyCommands
import resourceCommands

logging.basicConfig(level=logging.INFO)

client = discord.Client()

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

    """
    Hello - Test command, replies with "Hello!"
    """
    if message.content[len(config.CommandPrefix):].startswith('hello'):
        await message.channel.send('Hello!')

    """
    Help - lists all commands
    """
    if message.content[len(config.CommandPrefix):].startswith('help'):
        embed = discord.Embed(title=f"Help", description=f"")
        embed.add_field(name=f"Hello - `{config.CommandPrefix}hello`", value=f"A test command, simply replies hello", inline=False)
        embed.add_field(name=f"Account - `{config.CommandPrefix}account`", value=f"Sets up an account for using commands to do with money", inline=False)
        embed.add_field(name=f"Balance - `{config.CommandPrefix}balance`", value=f"View account balance", inline=False)
        embed.add_field(name=f"Hug - `{config.CommandPrefix}hug <mention>`", value=f"Hugs a user. Keep adding mentions to do a bigger group hug", inline=False)
        embed.add_field(name=f"Daily - `{config.CommandPrefix}daily`", value=f"Collect your daily money reward", inline=False)
        embed.add_field(name=f"Loot - `{config.CommandPrefix}loot`", value=f"Searches the recent messages for money", inline=False)
        embed.add_field(name=f"Inventory - `{config.CommandPrefix}inventory`", value=f"View your inventory", inline=False)
        embed.add_field(name=f"Mine - `{config.CommandPrefix}mine`", value=f"Mines for minerals and ores", inline=False)
        embed.add_field(name=f"Market - `{config.CommandPrefix}market`", value=f"Views the market prices", inline=False)
        embed.add_field(name=f"Market Buy - `{config.CommandPrefix}market buy <item>`", value=f"Buys 1 of an item on the market", inline=False)
        embed.add_field(name=f"Market Sell - `{config.CommandPrefix}market sell <item>`", value=f"Sells 1 of an item on the market", inline=False)

        await message.channel.send(embed=embed)

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

    """
    Account - Command to create an account
    """
    if message.content[len(config.CommandPrefix):].startswith("account"):
        await accountCommands.CreateAccount(message)

    """
    Balance - Command to check account balance. If user has no account, one will be created
    """
    if message.content[len(config.CommandPrefix):].startswith("balance"):
        await accountCommands.ViewBalance(message)

    """
    Hug - Hug another user. Implement random gif from giphy
    """
    if message.content[len(config.CommandPrefix):].startswith("hug"):
        if not message.mentions:
            await message.channel.send(f"You need to mention at least 1 user")
        elif len(message.mentions) == 1:
            await message.channel.send(f"**{message.mentions[0].name}**, you have been hugged by **{message.author.name}**")
        else:
            await message.channel.send(f"**{', '.join([x.name for x in message.mentions])}**, you have all been hugged by **{message.author.name}**")

    """
    Daily - base amount of $config.Daily_Base_Amount, multiplier increases by 1 each day, resets if not run for more than a day
    """
    if message.content[len(config.CommandPrefix):].startswith("daily"):
        await moneyCommands.Daily(message)

    """
    Loot - randomly generates between $0 and $config.Loot_Max with a minimum time between messages
    """
    if message.content[len(config.CommandPrefix):].startswith("loot"):
        await moneyCommands.Loot(message)

    """
    Inventory - View inventory
    """
    if message.content[len(config.CommandPrefix):].startswith("inventory"):
        await accountCommands.ViewInventory(message)

    """
    Mine - Mine for ores/minerals. Requires a pickaxe
    """
    if message.content[len(config.CommandPrefix):].startswith("mine"):
        await resourceCommands.Mine(message)

    """
    Market - Time to add subcommands. 
        Market - View all items and prices
        Market Buy <item> - buy an item
        Market Sell <item> - sell an item
    """
    if message.content[len(config.CommandPrefix):].startswith("market"):

        with open("userDetails.json", "r") as details: #Load the user details
            JsonDetails = json.loads(details.read())

        if str(message.author.id) not in JsonDetails:
            await message.channel.send(f"{message.author.name}, you don't have an account yet. Run `{config.CommandPrefix}account` to set one up, then try this command again")
            return

        with open("items.json", "r") as details: #Load the item details
            AllItems = json.loads(details.read())

        if len(message.content.split(" ")) == 1:
            await marketCommands.MarketView(message)

        elif len(message.content.split(" ")) == 3:
            #buy/sell

            if message.content.split(" ")[1] == "buy":
                await marketCommands.MarketBuy(message)

            elif message.content.split(" ")[1] == "sell":
                await marketCommands.MarketSell(message)


client.run(creds.SecretKey)