import json
import discord

import config

async def MarketParent(message: discord.Message) -> None:
    
    with open("userDetails.json", "r") as details: #Load the user details
        JsonDetails = json.loads(details.read())

    if str(message.author.id) not in JsonDetails:
        await message.channel.send(f"{message.author.name}, you don't have an account yet. Run `{config.CommandPrefix}account` to set one up, then try this command again")
        return

    if len(message.content.split(" ")) == 1:
        await MarketView(message)

    elif len(message.content.split(" ")) == 3:
        #buy/sell

        if message.content.split(" ")[1] == "buy":
            await MarketBuy(message)

        elif message.content.split(" ")[1] == "sell":
            await MarketSell(message)

async def MarketView(message: discord.Message) -> None:

    #Load the details of all the items
    with open("items.json", "r") as details:
        AllItems = json.loads(details.read())

    #Start creating a message to reply with
    embed = discord.Embed(title="Market", description=f"Here are all the items that you can buy and sell\nTo buy an item, use `{config.CommandPrefix}market buy <item name in grey box>`\nTo sell an item, use `{config.CommandPrefix}market sell <item name in grey box>`")

    #For every item in existence, add its etails to the market listing
    for item in [(k, v) for k, v in AllItems['items'].items()]:
        embed.add_field(name=f":{item[1]['emoji']}: {item[1]['name']}", value=f"{item[1]['description']} - `{item[0]}` - ${item[1]['cost']}", inline=True)

    embed.set_footer(text="Thanks for using Celeste")

    #Send out the market listing
    await message.channel.send(embed=embed)


async def MarketBuy(message: discord.Message) -> None:
    #Load the details of all items and all users
    with open("items.json", "r") as details:
        AllItems = json.loads(details.read())

    with open("userDetails.json", "r") as details:
        JsonDetails = json.loads(details.read())

    if message.content.split(" ")[2] in AllItems['items']: #Check that the item exists

        if JsonDetails[str(message.author.id)]['balance'] >= AllItems['items'][message.content.split(" ")[2]]['cost']: #Check that the user has enough money to buy the item
            #Set item key to item_data value in inventory, then splice in quantity
            if message.content.split(" ")[2] in JsonDetails[str(message.author.id)]['inventory']:
                #Just add to quantity
                JsonDetails[str(message.author.id)]['inventory'][message.content.split(" ")[2]]['quantity'] += 1
            else:
                #We need to construct the item
                JsonDetails[str(message.author.id)]['inventory'][message.content.split(" ")[2]] = AllItems['items'][message.content.split(" ")[2]]['item_data']
                JsonDetails[str(message.author.id)]['inventory'][message.content.split(" ")[2]]['quantity'] = 1

            JsonDetails[str(message.author.id)]['balance'] -= AllItems['items'][message.content.split(" ")[2]]['cost'] #What did it cost? The price

            #Send a confirmation message
            await message.channel.send(f"Successfully bought {AllItems['items'][message.content.split(' ')[2]]['name']} for ${AllItems['items'][message.content.split(' ')[2]]['cost']}")

        else:
            await message.channel.send(":x: Sorry, you don't have enough money for that")
    else:
        await message.channel.send(f":x: Item \"{message.content.split(' ')[2]}\" doesn't exist")

    #Write all changes back to disk
    with open("userDetails.json", "w") as details:
        details.write(json.dumps(JsonDetails))


async def MarketSell(message: discord.Message) -> None:
    #Load in the details of all items and all users
    with open("items.json", "r") as details:
        AllItems = json.loads(details.read())

    with open("userDetails.json", "r") as details:
        JsonDetails = json.loads(details.read())

    if message.content.split(" ")[2] in AllItems['items']: #Check that the item exists

        if message.content.split(' ')[2] in JsonDetails[str(message.author.id)]['inventory']: #Check that the user actually owns the item

            JsonDetails[str(message.author.id)]['inventory'][message.content.split(" ")[2]]['quantity'] -= 1 #remove 1 of the item

            if JsonDetails[str(message.author.id)]['inventory'][message.content.split(" ")[2]]['quantity'] == 0: #if there are none left, remove the item from the inventory entirely
                del JsonDetails[str(message.author.id)]['inventory'][message.content.split(" ")[2]]

            JsonDetails[str(message.author.id)]['balance'] += AllItems['items'][message.content.split(" ")[2]]['cost'] #Give the money

            #Send a confirmation message
            await message.channel.send(f"Successfully sold {AllItems['items'][message.content.split(' ')[2]]['name']} for ${AllItems['items'][message.content.split(' ')[2]]['cost']}")

        else:
            await message.channel.send(f":x: You dont have any {message.content.split(' ')[2]}")
    else:
        await message.channel.send(f":x: Item \"{message.content.split(' ')[2]}\" doesn't exist")

    #Write all changes back to disk
    with open("userDetails.json", "w") as details:
        details.write(json.dumps(JsonDetails))