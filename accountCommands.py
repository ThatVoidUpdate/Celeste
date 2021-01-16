import json
import discord

import config

async def CreateAccount(message: discord.Message) -> None:
    with open("userDetails.json", "r") as details: #Load the user details
        JsonDetails = json.loads(details.read())

    if str(message.author.id) in JsonDetails:
        await message.channel.send(f"You already have an account")
        return

    JsonDetails[str(message.author.id)] = config.defaultUserDict

    with open("userDetails.json", "w") as details:
        details.write(json.dumps(JsonDetails))

    await message.channel.send(f"Successfully created an account for {message.author.name}")

async def ViewBalance(message: discord.Message) -> None:
    with open("userDetails.json", "r") as details: #Load the user details
        JsonDetails = json.loads(details.read())

    if str(message.author.id) not in JsonDetails:
        await message.channel.send(f"{message.author.name}, you don't have an account yet. Run `{config.CommandPrefix}account` to set one up, then try this command again")
        return

    await message.channel.send(f":information_source: {message.author.name}, your balance is ${JsonDetails[str(message.author.id)]['balance']}")

async def ViewInventory(message: discord.Message) -> None:
    with open("userDetails.json", "r") as details: #Load the user details
        JsonDetails = json.loads(details.read())

    if str(message.author.id) not in JsonDetails:
        await message.channel.send(f"{message.author.name}, you don't have an account yet. Run `{config.CommandPrefix}account` to set one up, then try this command again")
        return

    userInventory = [(k, v) for k, v in JsonDetails[str(message.author.id)]['inventory'].items()]

    with open("items.json", "r") as details: #Load the item details
        AllItems = json.loads(details.read())

    if not userInventory:
        await message.channel.send(f"{message.author.name}, you have no items")
        return

    embed = discord.Embed(title=f"{message.author.name}'s Inventory", description=f"")
    for RawItem in userInventory:
        if RawItem[0] in AllItems['items']:
            embed.add_field(name=f":{AllItems['items'][RawItem[0]]['emoji']}: {AllItems['items'][RawItem[0]]['name']} x{RawItem[1]['quantity']}", value=f"{AllItems['items'][RawItem[0]]['description']}\nWorth ${AllItems['items'][RawItem[0]]['cost']}\n`{RawItem[0]}`", inline=True)

    await message.channel.send(embed=embed)