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
    PossibleResults = [x for x in AllItems['items'] if 'mine_chance' in AllItems['items'][x]['item_data']]
    MineChances = [(x, float(AllItems['items'][x]['item_data']['mine_chance'])) for x in PossibleResults]
    
    MineResults = [x[0] for x in MineChances if random.uniform(0, 1) < x[1]]


    for item in MineResults:
        if item in JsonDetails[str(message.author.id)]['inventory']:
            JsonDetails[str(message.author.id)]['inventory'][item]['quantity'] += 1
        else:
            JsonDetails[str(message.author.id)]['inventory'][item] = {"quantity": 1}

    JsonDetails[str(message.author.id)]['inventory'][pickaxeItem[0]]['durability'] -= 1

    if not MineResults:
        ret = "You went mining, but sadly you didnt get anything\n"
    else:
        ret = f"You went mining, and got:\n"

        for item in MineResults:
            ret += f"{AllItems['items'][item]['name']} x1\n"

    if JsonDetails[str(message.author.id)]['inventory'][pickaxeItem[0]]['durability'] == 0:
        ret += "Sadly your pickaxe broke"
        del JsonDetails[str(message.author.id)]['inventory'][pickaxeItem[0]]

    else:
        ret += f"Your pickaxe now has {JsonDetails[str(message.author.id)]['inventory'][pickaxeItem[0]]['durability']} uses left"

    await message.channel.send(ret)

    with open("userDetails.json", "w") as details:
        details.write(json.dumps(JsonDetails))


async def Chop(message: discord.Message) -> None:
    #Check user has account
    with open("userDetails.json", "r") as details: #Load the user details
        JsonDetails = json.loads(details.read())

    if str(message.author.id) not in JsonDetails:
        await message.channel.send(f"{message.author.name}, you don't have an account yet. Run `{config.CommandPrefix}account` to set one up, then try this command again")
        return

    #Check user has axe
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

    #find all possible chop results
    PossibleResults = [x for x in AllItems['items'] if 'chop_chance' in AllItems['items'][x]['item_data']]
    ChopChances = [(x, float(AllItems['items'][x]['item_data']['chop_chance'])) for x in PossibleResults]
    
    ChopResults = [x[0] for x in ChopChances if random.uniform(0, 1) < x[1]]
    
    #Give the user the items
    for item in ChopResults:

        if item in JsonDetails[str(message.author.id)]['inventory']:
            JsonDetails[str(message.author.id)]['inventory'][item]['quantity'] += 1
        else:
            JsonDetails[str(message.author.id)]['inventory'][item] = {"quantity": 1}

        JsonDetails[str(message.author.id)]['inventory'][axeItem[0]]['durability'] -= 1

    if not ChopResults:
        ret = "You went chopping, but sadly you didnt get anything\n"
    else:
        ret = f"You chopped down some trees, and got:\n"

        for item in ChopResults:
            ret += f"{AllItems['items'][item]['name']} x1\n"

    if JsonDetails[str(message.author.id)]['inventory'][axeItem[0]]['durability'] == 0:
        ret += "Sadly your axe broke"
        del JsonDetails[str(message.author.id)]['inventory'][axeItem[0]]

    else:
        ret += f"Your axe now has {JsonDetails[str(message.author.id)]['inventory'][axeItem[0]]['durability']} uses left"

    #Write the changes back to disk
    with open("userDetails.json", "w") as details:
        details.write(json.dumps(JsonDetails))

    await message.channel.send(ret)

async def Smelt(message: discord.Message) -> None:
    #check the user passed in an item
    if len(message.content.split(' ')) != 2:
        await message.channel.send(f":x: Please pass in one item to be smelted")
        return

    itemName = message.content.split(' ')[1]


    #check for user account
    with open("userDetails.json", "r") as details: #Load the user details
        JsonDetails = json.loads(details.read())

    if str(message.author.id) not in JsonDetails:
        await message.channel.send(f"{message.author.name}, you don't have an account yet. Run `{config.CommandPrefix}account` to set one up, then try this command again")
        return

    #check user has wood
    if 'wood' not in JsonDetails[str(message.author.id)]['inventory']:
        await message.channel.send(f":x: You don't have any wood")
        return

    #check item exists
    with open("items.json", "r") as details:
        AllItems = json.loads(details.read())

    if itemName not in AllItems['items']: #Check that the item exists
        await message.channel.send(f":x: Item \"{itemName}\" doesn't exist")
        return

    #check that the item is smeltable
    if "smelted" not in AllItems['items'][itemName]['item_data']:
        await message.channel.send(f":x: You can't smelt {itemName}")
        return

    #check user has item
    if itemName not in JsonDetails[str(message.author.id)]['inventory']:
        await message.channel.send(f":x: You don't have any {itemName}")
        return

    smeltingItem = AllItems['items'][itemName]
    resultItemName = smeltingItem['item_data']['smelted']

    #remove 1 of item
    JsonDetails[str(message.author.id)]['inventory'][itemName]['quantity'] -= 1

    if JsonDetails[str(message.author.id)]['inventory'][itemName]['quantity'] == 0: #if there are none left, remove the item from the inventory entirely
        del JsonDetails[str(message.author.id)]['inventory'][itemName]

    #remove 1 wood
    JsonDetails[str(message.author.id)]['inventory']['wood']['quantity'] -= 1

    if JsonDetails[str(message.author.id)]['inventory']['wood']['quantity'] == 0: #if there are none left, remove the item from the inventory entirely
        del JsonDetails[str(message.author.id)]['inventory']['wood']

    #give one of smelt result
    if resultItemName in JsonDetails[str(message.author.id)]['inventory']:
        JsonDetails[str(message.author.id)]['inventory'][resultItemName]['quantity'] += 1
    else:
        JsonDetails[str(message.author.id)]['inventory'][resultItemName] = {"quantity": 1}
    
    await message.channel.send(f"You smelted {smeltingItem['name']} and got {AllItems['items'][resultItemName]['name']}")

    #Write all changes back to disk
    with open("userDetails.json", "w") as details:
        details.write(json.dumps(JsonDetails))