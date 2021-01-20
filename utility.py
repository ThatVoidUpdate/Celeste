import json
import discord

def UserHasAccount(userID: str) -> bool:
    #check for user account
    with open("userDetails.json", "r") as details: #Load the user details
        JsonDetails = json.loads(details.read())

    return str(userID) in JsonDetails

    #if str(userID) not in JsonDetails:
    #    await message.channel.send(f"{message.author.name}, you don't have an account yet. Run `{config.CommandPrefix}account` to set one up, then try this command again")
    #    return

def CheckItemExists(itemID: str) -> bool:
    with open("items.json", "r") as details:
        AllItems = json.loads(details.read())

    return itemID in AllItems['items']

def UserHasItem(userID: str, itemID: str) -> bool:
    with open("userDetails.json", "r") as details: #Load the user details
        JsonDetails = json.loads(details.read())

    return itemID in JsonDetails[str(userID)]['inventory']

    #if 'wood' not in JsonDetails[str(userID)]['inventory']:
    #    await message.channel.send(f":x: You don't have any wood")
    #    return

def GetItemData(itemID: str) -> dict:
    with open("items.json", "r") as details:
        AllItems = json.loads(details.read())
    
    return AllItems['items'][itemID]

def GetUserInventory(userID: str) -> list:
    with open("userDetails.json", "r") as details: #Load the user details
        JsonDetails = json.loads(details.read())

    return list([(k, v) for k, v in JsonDetails[str(userID)]['inventory'].items()])

def GiveUserItem(userID: str, itemID: str, amount: int) -> None:
    with open("userDetails.json", "r") as details: #Load the user details
        JsonDetails = json.loads(details.read())

    if itemID in JsonDetails[str(userID)]['inventory']:
        JsonDetails[str(userID)]['inventory'][itemID]['quantity'] += amount
    else:
        JsonDetails[str(userID)]['inventory'][itemID] = {"quantity": amount}

    SaveUserData(JsonDetails)

def TakeUserItem(userID: str, itemID: str) -> None:
    with open("userDetails.json", "r") as details: #Load the user details
        JsonDetails = json.loads(details.read())

    JsonDetails[str(userID)]['inventory'][itemID]['quantity'] -= 1

    if JsonDetails[str(userID)]['inventory'][itemID]['quantity'] == 0: #if there are none left, remove the item from the inventory entirely
        del JsonDetails[str(userID)]['inventory'][itemID]
    
    SaveUserData(JsonDetails)

def SaveUserData(data: str) -> None:
    with open("userDetails.json", "w") as details:
        details.write(json.dumps(data))

def SetUserItemData(userID: str, itemID: str, key: str, value) -> None:
    with open("userDetails.json", "r") as details: #Load the user details
        JsonDetails = json.loads(details.read())
    JsonDetails[str(userID)]['inventory'][itemID][key] = value
    
    SaveUserData(JsonDetails)

def AdjustUserItemData(userID: str, itemID: str, key: str, delta: int) -> None:
    with open("userDetails.json", "r") as details: #Load the user details
        JsonDetails = json.loads(details.read())
    JsonDetails[str(userID)]['inventory'][itemID][key] += delta
    
    SaveUserData(JsonDetails)

def GetUserItem(userID: str, itemID: str) -> tuple:
    with open("userDetails.json", "r") as details: #Load the user details
        JsonDetails = json.loads(details.read())

    return (itemID, JsonDetails[str(userID)]['inventory'][itemID])