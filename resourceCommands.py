import json
import random
import discord

import config
import utility

async def Mine(message: discord.Message) -> None:
    if not utility.UserHasAccount(message.author.id):
        await message.channel.send(f"{message.author.name}, you don't have an account yet. Run `{config.CommandPrefix}account` to set one up, then try this command again")
        return

    with open("items.json", "r") as details: #Load the item details
        AllItems = json.loads(details.read())

    userInventory = utility.GetUserInventory(str(message.author.id))

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
        utility.GiveUserItem(str(message.author.id), item, 1)


    if not MineResults:
        ret = "You went mining, but sadly you didnt get anything\n"
    else:
        ret = f"You went mining, and got:\n"

        for item in MineResults:
            ret += f"{AllItems['items'][item]['name']} x1\n"

    #Remove 1 pick durability
    utility.AdjustUserItemData(message.author.id, pickaxeItem[0], 'durability', -1)

    #Check if pick broke
    if utility.GetUserItem(message.author.id, pickaxeItem[0])[1]['durability'] == 0:
        ret += "Sadly your pickaxe broke"
        utility.TakeUserItem(message.author.id, pickaxeItem[0])
    else:
        ret += f"Your pickaxe now has {utility.GetUserItem(message.author.id, pickaxeItem[0])[1]['durability']} uses left"

    await message.channel.send(ret)

async def Chop(message: discord.Message) -> None:
    #Check user has account
    if not utility.UserHasAccount(message.author.id):
        await message.channel.send(f"{message.author.name}, you don't have an account yet. Run `{config.CommandPrefix}account` to set one up, then try this command again")
        return

    #Check user has axe
    userInventory = utility.GetUserInventory(str(message.author.id))

    with open("items.json", "r") as details: #Load the item details
        AllItems = json.loads(details.read())

    axeItem = None
    for RawItem in userInventory:
        if AllItems['items'][RawItem[0]]['type'] == "pickaxe":
            axeItem = (RawItem[0], AllItems['items'][RawItem[0]])

    if axeItem is None:
        await message.channel.send(f":x: You own no pickaxes")
        return

    #find all possible chop results
    PossibleResults = [x for x in AllItems['items'] if 'chop_chance' in AllItems['items'][x]['item_data']]
    ChopChances = [(x, float(AllItems['items'][x]['item_data']['chop_chance'])) for x in PossibleResults]

    ChopResults = [x[0] for x in ChopChances if random.uniform(0, 1) < x[1]]

    #Give the user the items
    for item in ChopResults:
        utility.GiveUserItem(str(message.author.id), item, 1)


    utility.AdjustUserItemData(message.author.id, axeItem[0], 'durability', -1)

    if not ChopResults:
        ret = "You went chopping, but sadly you didnt get anything\n"
    else:
        ret = f"You chopped down some trees, and got:\n"

        for item in ChopResults:
            ret += f"{AllItems['items'][item]['name']} x1\n"

    if utility.GetUserItem(message.author.id, axeItem[0])[1]['durability'] == 0:
        ret += "Sadly your pickaxe broke"
        utility.TakeUserItem(message.author.id, axeItem[0])
    else:
        ret += f"Your pickaxe now has {utility.GetUserItem(message.author.id, axeItem[0])[1]['durability']} uses left"

    await message.channel.send(ret)

async def Smelt(message: discord.Message) -> None:
    if not utility.UserHasAccount(message.author.id):
        await message.channel.send(f"{message.author.name}, you don't have an account yet. Run `{config.CommandPrefix}account` to set one up, then try this command again")
        return

    #check the user passed in an item
    if len(message.content.split(' ')) != 2:
        await message.channel.send(f":x: Please pass in one item to be smelted")
        return

    itemName = message.content.split(' ')[1]

    #check user has wood
    if not utility.UserHasItem(message.author.id, 'wood'):
    #if 'wood' not in JsonDetails[str(message.author.id)]['inventory']:
        await message.channel.send(f":x: You don't have any wood")
        return

    #check item exists
    if not utility.CheckItemExists(itemName):
        await message.channel.send(f":x: Item \"{itemName}\" doesn't exist")
        return

    itemDetails = utility.GetItemData(itemName)

    #check that the item is smeltable
    if "smelted" not in itemDetails['item_data']:
        await message.channel.send(f":x: You can't smelt {itemName}")
        return

    #check user has item
    if not utility.UserHasItem(str(message.author.id), itemName):
        await message.channel.send(f":x: You don't have any {itemName}")
        return

    resultItemName = itemDetails['item_data']['smelted']
    resultItem = utility.GetItemData(resultItemName)

    #remove 1 of item
    utility.TakeUserItem(message.author.id, itemName)

    #remove 1 wood
    utility.TakeUserItem(message.author.id, 'wood')

    #give one of smelt result
    utility.GiveUserItem(str(message.author.id), resultItemName, 1)
    
    await message.channel.send(f"You smelted {itemDetails['name']} and got {resultItem['name']}")

async def Explore(message: discord.Message) -> None:
    #check user has account
    #check user has boots
    #choose a random destination/no destination
    #get loot
    #write all changes back to disk
    pass