# Hall_Of_Fame_Bot

A discord bot, coded in python, designed to retrieve and send the most messages most reacted to with a given "emote" in a discord server

## usage
A discord bot account and server are required.
More information can be found [here](https://discordpy.readthedocs.io/en/stable/discord.html).

replace placeholder bot token and channel ID before running. once the script is running Hall Of Fame Bot will respond to the following command:

- `!top EMOTE`: where emote is replaced with the reaction/emote (whatever you want to call it!)

## TO DO
- bot currently does not handle long messages well, and faults. figure out a way to parse longer messages.
- find out a way to exclude messages reacted to that were sent by the bot