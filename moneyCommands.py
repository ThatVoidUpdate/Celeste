import json
import random
import time
import discord

import config

async def Daily(message: discord.Message) -> None:
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

async def Loot(message: discord.Message) -> None:
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