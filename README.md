# Celeste
This discord bot is the product of my slight frustration with some of the features of Mantaro (https://github.com/Mantaro/MantaroBot). However, it is a completely clean-room recreation, and any similarities to the code of Mantaro is entirely coincidental.

All of Celeste's internal state is shared between any servers it is in, so things like balance, inventory etc will be the same in all servers. As such, there are no commands to give items or money, as this would break the economy.

If you wish to run your own version of this bot, then you will have to create your own discord bot using these instructions https://discordpy.readthedocs.io/en/latest/discord.html, then create a creds.py file with this contents:
```python
SecretKey = 'bot account secret key here'
```