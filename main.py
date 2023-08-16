import os
import discord
import json
from discord.ext import commands
import services.Security

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
    token = data["token"]

client.remove_command("help")


@client.command()
@commands.is_owner()
async def load(ctx, extension):
    """
    This Python function loads a cog extension and sends a message confirming that the extension has been loaded.

    :param ctx: ctx is the context object, which contains information about the command being executed, such as the message,
    the channel, the author, etc
    :param extension: The "extension" parameter is a string that represents the name of the cog file that you want to load.
    Cogs are a way to organize and modularize your code in a Discord bot. Each cog is a separate file that contains a set of
    related commands and event handlers
    """
    await client.load_extension(f'cogs.{extension}')
    await ctx.send(f'The extension {extension} has been loaded')


@client.command()
@commands.is_owner()
async def unload(ctx, extension):
    """
    This Python function unloads a specific extension in a Discord bot and sends a message confirming the action.

    :param ctx: The `ctx` parameter stands for "context" and represents the context in which the command is being executed.
    It contains information about the message, the user who sent the message, the channel where the message was sent, and
    other relevant details
    :param extension: The `extension` parameter is a string that represents the name of the cog (a Python file containing
    commands and event listeners) that you want to unload. The `unload` command unloads the specified cog from the bot's
    list of loaded cogs, effectively disabling its functionality
    """

    await client.unload_extension(f'cogs.{extension}')
    await ctx.send(f'The extension {extension} has been unloaded')


@client.command()
@commands.is_owner()
async def reload(ctx, extension):
    """
    This Python function allows the owner of the bot to reload a specific cog (extension) in the bot.

    :param ctx: The `ctx` parameter stands for "context" and represents the context in which the command is being executed.
    It contains information about the message, the user who sent the message, the channel the message was sent in, and other
    relevant details
    :param extension: The `extension` parameter is a string that represents the name of the cog (a module containing
    commands and event handlers) that you want to reload. It should be the name of the Python file without the `.py`
    extension. For example, if you have a cog named `example.py`, you
    """
    await client.unload_extension(f'cogs.{extension}')
    await client.load_extension(f'cogs.{extension}')
    await ctx.send(f'The extension {extension} has been reloaded')


@client.event
async def on_command_error(ctx, error):
    """
    This function handles the event when a command is not found and sends a message indicating that an invalid command was
    used.

    :param ctx: ctx stands for "context" and it represents the context in which the command was invoked. It contains
    information about the message, the channel, the author, and other relevant details
    :param error: The `error` parameter in the `on_command_error` function is the error that occurred when a command was
    executed. It can be any type of error, such as a `CommandNotFound` error when the user enters an invalid command
    """
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Invalid command used.")


@client.event
async def setup_hook(self=None):
    """
    The `setup_hook` function loads all Python files in the "cogs" directory as extensions for the client and prints the
    name of each loaded cog.

    :param self: In the given code snippet, `self` is a reference to the instance of the class that the `setup_hook` method
    belongs to. It is commonly used in object-oriented programming to refer to the current instance of a class. In this
    case, it is used to access the `client` object
    """
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await client.load_extension(f'cogs.{filename[:-3]}')
            print(f"Loaded Cog: {filename[:-3]}")


client.run(token)
