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

async def GiveItem(message: discord.Message) -> None:
    #check user has account
    with open("userDetails.json", "r") as details: #Load the user details
        JsonDetails = json.loads(details.read())

    if str(message.author.id) not in JsonDetails:
        await message.channel.send(f"{message.author.name}, you don't have an account yet. Run `{config.CommandPrefix}account` to set one up, then try this command again")
        return

    #check correct amount of arguments were passed
    if len(message.content.split(' ')) != 3:
        await message.channel.send(f":x: Either no item was specified, no user was specified, or too many arguments were given")
        return

    #check a user was mentioned
    if len(message.mentions) != 1:
        await message.channel.send(f":x: No user was specified")
        return

    recipient = message.mentions[0]

    #check recipient has account
    if str(recipient.id) not in JsonDetails:
        await message.channel.send(f"{recipient.name} doesn't have an account yet. They need to run  `{config.CommandPrefix}account` to set one up, then try this command again")
        return

    #check item exists
    itemName = [x for x in message.content.split(' ') if config.CommandPrefix not in x and "@" not in x][0]

    with open("items.json", "r") as details:
        AllItems = json.loads(details.read())

    if itemName not in AllItems['items']: #Check that the item exists
        await message.channel.send(f":x: Item \"{itemName}\" doesn't exist")
        return

    #check user has item
    if itemName not in JsonDetails[str(message.author.id)]['inventory']:
        await message.channel.send(f":x: You don't have any {itemName}")
        return

    #remove 1 of item from user
    JsonDetails[str(message.author.id)]['inventory'][itemName]['quantity'] -= 1

    if JsonDetails[str(message.author.id)]['inventory'][itemName]['quantity'] == 0: #if there are none left, remove the item from the inventory entirely
        del JsonDetails[str(message.author.id)]['inventory'][itemName]

    #give 1 of item to recipient
    if itemName in JsonDetails[str(recipient.id)]['inventory']:
        JsonDetails[str(recipient.id)]['inventory'][itemName]['quantity'] += 1
    else:
        JsonDetails[str(recipient.id)]['inventory'][itemName] = {"quantity": 1}

    await message.channel.send(f"{recipient.name}, {message.author.name} just gave you 1 {AllItems['items'][itemName]['name']}")

    #Write all changes back to disk
    with open("userDetails.json", "w") as details:
        details.write(json.dumps(JsonDetails))

async def GiveMoney(message: discord.Message) -> None:
     #check user has account
    with open("userDetails.json", "r") as details: #Load the user details
        JsonDetails = json.loads(details.read())

    if str(message.author.id) not in JsonDetails:
        await message.channel.send(f"{message.author.name}, you don't have an account yet. Run `{config.CommandPrefix}account` to set one up, then try this command again")
        return

    #check correct amount of arguments were passed
    if len(message.content.split(' ')) != 3:
        await message.channel.send(f":x: Either no amount was specified, no user was specified, or too many arguments were given")
        return

    #check a user was mentioned
    if len(message.mentions) != 1:
        await message.channel.send(f":x: No user was specified")
        return

    recipient = message.mentions[0]

    #check recipient has account
    if str(recipient.id) not in JsonDetails:
        await message.channel.send(f"{recipient.name} doesn't have an account yet. They need to run  `{config.CommandPrefix}account` to set one up, then try this command again")
        return

    #check other argument was number
    amount = [x for x in message.content.split(' ') if config.CommandPrefix not in x and "@" not in x][0]

    try:
        amount = int(amount)
    except:
        await message.channel.send(f":x: {amount} is not a number")
        return

    if amount <= 0:
        await message.channel.send(f":x: {amount} has to be above 0")
        return

    #check user has enough money
    if amount > int(JsonDetails[str(message.author.id)]['balance']):
        await message.channel.send(f":x: You don't have enough money for that")
        return

    #Give the money
    JsonDetails[str(message.author.id)]['balance'] = str(int(JsonDetails[str(message.author.id)]['balance']) - amount)
    JsonDetails[str(recipient.id)]['balance'] = str(int(JsonDetails[str(recipient.id)]['balance']) + amount)

    await message.channel.send(f"{recipient.name}, {message.author.name} just gave you ${amount}")

    #Write all changes back to disk
    with open("userDetails.json", "w") as details:
        details.write(json.dumps(JsonDetails))