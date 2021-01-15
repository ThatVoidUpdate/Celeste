import logging
import sys
import os
import json
import time
import random
import discord

import creds
import config
import marketCommands

defaultUserDict = {"balance": 0, "daily_multiplier": 1, "last_daily": 0, "last_loot": 0, "inventory":{}}

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
        await reaction.message.channel.send(f"Thanks {' '.join([x.name for x in AllReactors])}")


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
        ret = """Help:
`hello` - Test command, simply says hello
`account` - Sets up an account for use with commands that require money
`balance` - View your balance
`hug <mention> [mention]` - Hugs another user. Keep adding mentions to hug more people
`daily` - Collect yuor daily money reward
`loot` - Scour the recent messages for money
`inventory` - View your inventory
`mine` - Use your pickaxe to mine for ores and minerals
`market` - View the market
`market buy <item>` - Buy an item
`market sell <item>` - Sell an item 
"""
        await message.channel.send(ret)

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
        with open("userDetails.json", "r") as details: #Load the user details
            JsonDetails = json.loads(details.read())

        if str(message.author.id) in JsonDetails:
            await message.channel.send(f"You already have an account")
            return

        JsonDetails[str(message.author.id)] = defaultUserDict

        with open("userDetails.json", "w") as details:
            details.write(json.dumps(JsonDetails))

        await message.channel.send(f"Successfully created an account for {message.author.name}")

    """
    Balance - Command to check account balance. If user has no account, one will be created
    """
    if message.content[len(config.CommandPrefix):].startswith("balance"):
        print(f"Attempting to check balance for user id {message.author.id}")

        with open("userDetails.json", "r") as details: #Load the user details
            JsonDetails = json.loads(details.read())

        if str(message.author.id) not in JsonDetails:
            await message.channel.send(f"{message.author.name}, you don't have an account yet. Run `{config.CommandPrefix}account` to set one up, then try this command again")
            return

        await message.channel.send(f":information_source: {message.author.name}, your balance is ${JsonDetails[str(message.author.id)]['balance']}")

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
        #get last daily interaction of user

        with open("userDetails.json", "r") as details: #Load the user details
            JsonDetails = json.loads(details.read())

        if str(message.author.id) not in JsonDetails:
            await message.channel.send(f"{message.author.name}, you don't have an account yet. Run `{config.CommandPrefix}account` to set one up, then try this command again")
            return

        currentEpochTime = time.time()
        timeDifference = currentEpochTime - int(JsonDetails[str(message.author.id)]['last_daily'])
        differenceTup = time.localtime(timeDifference)

        if int(JsonDetails[str(message.author.id)]['last_daily']) == 0:
            JsonDetails[str(message.author.id)]['daily_multiplier'] = 1
            JsonDetails[str(message.author.id)]['balance'] += config.Daily_Base_Amount
            JsonDetails[str(message.author.id)]['last_daily'] = time.time()

            with open("userDetails.json", "w") as details:
                details.write(json.dumps(JsonDetails))

            await message.channel.send(f":information_source: You can use this command once daily, and each day in a row you use it, you'll get more and more money. But if you miss a day, your streak goes back to 0. Today you got ${config.Daily_Base_Amount}, and your multiplier is `1x`")

        else:

            if differenceTup.tm_mday == 2:
                JsonDetails[str(message.author.id)]['daily_multiplier'] += config.Daily_Multiplier_Increment
                print(JsonDetails[str(message.author.id)]['daily_multiplier'])
                JsonDetails[str(message.author.id)]['balance'] += config.Daily_Base_Amount * JsonDetails[str(message.author.id)]['daily_multiplier']
                JsonDetails[str(message.author.id)]['last_daily'] = time.time()

                with open("userDetails.json", "w") as details:
                    details.write(json.dumps(JsonDetails))

                await message.channel.send(f":moneybag: Congrats! You get ${config.Daily_Base_Amount * JsonDetails[str(message.author.id)]['daily_multiplier']}, and your multiplier is now `{JsonDetails[str(message.author.id)]['daily_multiplier']}x`")


            elif differenceTup.tm_mday > 2 or differenceTup.tm_mon > 1 or differenceTup.tm_year > 1970:
                JsonDetails[str(message.author.id)]['daily_multiplier'] = 1
                JsonDetails[str(message.author.id)]['balance'] += config.Daily_Base_Amount
                JsonDetails[str(message.author.id)]['last_daily'] = time.time()

                with open("userDetails.json", "w") as details:
                    details.write(json.dumps(JsonDetails))

                await message.channel.send(f":moneybag: Aww dang, you waited too long =(. You get ${config.Daily_Base_Amount}, and your daily multiplier is now `1x`")

            else:
                await message.channel.send(f":x: Too soon! (You can only use this command every 24 hours)")


    """
    Loot - randomly generates between $0 and $config.Loot_Max with a minimum time between messages
    """
    if message.content[len(config.CommandPrefix):].startswith("loot"):
        #get last daily interaction of user

        with open("userDetails.json", "r") as details: #Load the user details
            JsonDetails = json.loads(details.read())

        if str(message.author.id) not in JsonDetails:
            await message.channel.send(f"{message.author.name}, you don't have an account yet. Run `{config.CommandPrefix}account` to set one up, then try this command again")
            return

        currentEpochTime = time.time()
        timeDifference = currentEpochTime - int(JsonDetails[str(message.author.id)]['last_loot'])
        differenceTup = time.localtime(timeDifference)

        if int(JsonDetails[str(message.author.id)]['last_daily']) == 0:
            lootAmount = random.randint(1, config.Loot_Max)

            JsonDetails[str(message.author.id)]['last_loot'] = time.time()
            JsonDetails[str(message.author.id)]['balance'] += lootAmount

            with open("userDetails.json", "w") as details:
                details.write(json.dumps(JsonDetails))

            await message.channel.send(f":information_source: You can use this command once every 5 mins to search through chat for any money (anywhere from $1 to ${config.Loot_Max}). This time you got ${lootAmount}")

        else:
            if differenceTup.tm_min > 5 or differenceTup.tm_hour > 0 or differenceTup.tm_mday > 1 or differenceTup.tm_mon > 1 or differenceTup.tm_year > 1970:
                lootAmount = random.randint(1, config.Loot_Max)

                JsonDetails[str(message.author.id)]['last_loot'] = time.time()
                JsonDetails[str(message.author.id)]['balance'] += lootAmount

                with open("userDetails.json", "w") as details:
                    details.write(json.dumps(JsonDetails))

                await message.channel.send(f":moneybag: Rooting through the messages, you found ${lootAmount}")

            else:
                await message.channel.send(f":x: Too soon! (You can only use this command every 5 mins)")


    """
    Inventory - View inventory
    """
    if message.content[len(config.CommandPrefix):].startswith("inventory"):
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

        ret = f"{message.author.name}, your inventory is:\n"
        for RawItem in userInventory:
            if RawItem[0] in AllItems['items']:
                ret += f":{AllItems['items'][RawItem[0]]['emoji']}: {AllItems['items'][RawItem[0]]['name']} x {RawItem[1]['quantity']}\n"

        await message.channel.send(ret)

    """
    Mine - Mine for ores/minerals. Requires a pickaxe
    """
    if message.content[len(config.CommandPrefix):].startswith("mine"):
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