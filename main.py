import os
import discord
import json
from discord.ext import commands

# Author: Noah Funderburgh
# Date: 10/8/2020
# Description: Allows for Cogs be loaded, unloaded and reloaded
# so the program doesn't have to be restarted upon changes made
# Todo: No current plans to add anything to main.py

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = commands.Bot(command_prefix='.', intents=intents)
with open('mainConfig.json') as f:
    data = json.load(f)
    TOKEN = data["TOKEN"]

client.remove_command("help")


# This method loads an extension based on the parameter entered
# The person calling the command has to be the owner of the bot or else this won't work
#
# param: ctx, represents the context in which a command is being invoked under
# param: extension, the name of the extension to be loaded into the bot
# return: none
@client.command()
@commands.is_owner()
async def load(ctx, extension):
    await client.load_extension(f'cogs.{extension}')
    await ctx.send(f'The extension {extension} has been loaded')


# This method unloads an extension based on the parameter entered
# The person calling the command has to be the owner of the bot or else this won't work
#
# param: ctx, represents the context in which a command is being invoked under
# param: extension, the name of the extension to be unloaded into the bot
# return: none
@client.command()
@commands.is_owner()
async def unload(ctx, extension):
    await client.unload_extension(f'cogs.{extension}')
    await ctx.send(f'The extension {extension} has been unloaded')


# This method reload an extension based on the parameter entered
# The person calling the command has to be the owner of the bot or else this won't work
#
# param: ctx, represents the context in which a command is being invoked under
# param: extension, the name of the extension to be reloaded into the bot
# return: none
@client.command()
@commands.is_owner()
async def reload(ctx, extension):
    await client.unload_extension(f'cogs.{extension}')
    await client.load_extension(f'cogs.{extension}')
    await ctx.send(f'The extension {extension} has been reloaded')


# Provides the user with an error message in the same discord text channel
# informing them that the command they used doesn't exist
#
# param: ctx, represents the context in which a command is being invoked under
# param: error, the error that was raised
# return: none
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Invalid command used.")


# Loads the extensions in the cogs folder ending in .py upon startup
# Prints loaded cogs into console for debugging
@client.event
async def setup_hook():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await client.load_extension(f'cogs.{filename[:-3]}')
            print(f"Loaded Cog: {filename[:-3]}")


client.run(TOKEN)
