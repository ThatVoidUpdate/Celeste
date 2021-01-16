import json
import random
import discord

import config

async def Mine(message: discord.Message) -> None:
    with open("userDetails.json", "r") as details: #Load the user details
        JsonDetails = json.loads(details.read())

    if str(message.author.id) not in JsonDetails:
        await message.channel.send(f"{message.author.name}, you don't have an account yet. Run `{config.CommandPrefix}account` to set one up, then try this command again")
        return

    with open("items.json", "r") as details: #Load the item details
        AllItems = json.loads(details.read())

    userInventory = [(k, v) for k, v in JsonDetails[str(message.author.id)]['inventory'].items()]

    pickaxeItem = None
    for RawItem in userInventory:
        if AllItems['items'][RawItem[0]]['type'] == "pickaxe":
            pickaxeItem = (RawItem[0], AllItems['items'][RawItem[0]])

    if pickaxeItem is None:
        await message.channel.send(f":x: You own no pickaxes")
        return

    #we have the last pickaxe item in the user's inventory
    #randomly choose an ore or mineral to mine
    mineable = []

    for RawItem in [(k, v) for k, v in AllItems['items'].items()]:
        if RawItem[1]['type'] == "ore" or RawItem[1]['type'] == "mineral":
            mineable.append(RawItem)

    if not mineable:
        await message.channel.send(f":bangbang: A dev screwed up, there are no minable items")
        return

    result = random.choice(mineable)

    if result[0] in JsonDetails[str(message.author.id)]['inventory']:
        JsonDetails[str(message.author.id)]['inventory'][result[0]]['quantity'] += 1
    else:
        JsonDetails[str(message.author.id)]['inventory'][result[0]] = {"quantity": 1}

    JsonDetails[str(message.author.id)]['inventory'][pickaxeItem[0]]['durability'] -= 1



    ret = f"You got :{result[1]['emoji']}: {result[1]['name']}!\n"
    if JsonDetails[str(message.author.id)]['inventory'][pickaxeItem[0]]['durability'] == 0:
        ret += "Sadly your pickaxe broke"
        del JsonDetails[str(message.author.id)]['inventory'][pickaxeItem[0]]

    else:
        ret += f"Your pickaxe now has {JsonDetails[str(message.author.id)]['inventory'][pickaxeItem[0]]['durability']} uses left"

    with open("userDetails.json", "w") as details:
        details.write(json.dumps(JsonDetails))

    await message.channel.send(ret)

async def Chop(message: discord.Message) -> None:
    with open("userDetails.json", "r") as details: #Load the user details
        JsonDetails = json.loads(details.read())

    if str(message.author.id) not in JsonDetails:
        await message.channel.send(f"{message.author.name}, you don't have an account yet. Run `{config.CommandPrefix}account` to set one up, then try this command again")
        return

    with open("items.json", "r") as details: #Load the item details
        AllItems = json.loads(details.read())

    userInventory = [(k, v) for k, v in JsonDetails[str(message.author.id)]['inventory'].items()]

    axeItem = None
    for RawItem in userInventory:
        if AllItems['items'][RawItem[0]]['type'] == "axe":
            axeItem = (RawItem[0], AllItems['items'][RawItem[0]])

    if axeItem is None:
        await message.channel.send(f":x: You own no axes")
        return
    
    woodAmount = random.randint(1, 3)

    if 'wood' in JsonDetails[str(message.author.id)]['inventory']:
        JsonDetails[str(message.author.id)]['inventory']['wood']['quantity'] += woodAmount
    else:
        JsonDetails[str(message.author.id)]['inventory']['wood'] = {"quantity": woodAmount}

    JsonDetails[str(message.author.id)]['inventory'][axeItem[0]]['durability'] -= 1

    

    ret = f"You got {woodAmount} wood!\n"
    if JsonDetails[str(message.author.id)]['inventory'][axeItem[0]]['durability'] == 0:
        ret += "Sadly your axe broke"
        del JsonDetails[str(message.author.id)]['inventory'][axeItem[0]]

    else:
        ret += f"Your axe now has {JsonDetails[str(message.author.id)]['inventory'][axeItem[0]]['durability']} uses left"

    with open("userDetails.json", "w") as details:
        details.write(json.dumps(JsonDetails))

    await message.channel.send(ret)