import discord

import config

async def Hug(message: discord.Message) -> None:
    if not message.mentions:
        await message.channel.send(f"You need to mention at least 1 user")
    elif len(message.mentions) == 1:
        await message.channel.send(f"**{message.mentions[0].name}**, you have been hugged by **{message.author.name}**")
    else:
        await message.channel.send(f"**{', '.join([x.name for x in message.mentions])}**, you have all been hugged by **{message.author.name}**")

