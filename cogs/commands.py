import json
import random
import discord
from discord.ext import commands


# Author: Noah Funderburgh
# Date: 10/8/2020
# Description:
# Todo: Comment descriptions about each functions purpose, as well as parameters and return values.

class Commands(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        """
        The `on_ready` function sets the bot's status to "do not disturb" and the activity to "playing with my step bro"
        when the bot is ready.
        """
        await self.client.change_presence(status=discord.Status.do_not_disturb,
                                          activity=discord.Game('with my step bro'))
        print('Bot is ready.')

    @commands.command()
    async def help(self, ctx):
        """
        The `help` function sends an embedded message with a list of commands categorized by their functionality.

        :param ctx: The `ctx` parameter in the `help` command represents the context in which the command is being invoked.
        It contains information about the message, the channel, the server, and the user who triggered the command. It is an
        instance of the `commands.Context` class from the discord.py library
        """
        embed = discord.Embed(
            title="Step Sis Command List",
            # description="HI",
        )
        print('test.')
        embed.add_field(name=":musical_note: Music", value="`.helpMusic`", inline=True)
        embed.add_field(name=":joy: Reddit", value="`.helpReddit`", inline=True)
        embed.add_field(name=":game_die: Games", value="`.helpGame`", inline=True)
        embed.add_field(name=":tools: Utility", value="`.helpUtility`", inline=True)
        embed.add_field(name=":fire: Admin", value="`.helpAdmin`", inline=True)
        embed.add_field(name=":video_game: RPG", value="`.helpRPG`", inline=True)
        await ctx.send(embed=embed)

    @commands.command(aliases=['helputility'])
    async def helpUtility(self, ctx):
        """
        The `helpUtility` function sends an embedded message containing a list of utility commands to the Discord channel.

        :param ctx: The `ctx` parameter stands for "context" and it represents the context in which the command is being
        invoked. It contains information about the message, the channel, the server, and the user who triggered the command.
        It is an instance of the `commands.Context` class from the discord.py library
        """
        embed = discord.Embed(
            title=":tools: Utility Commands",
            description="`8ball`,`ping`,`troll`",
            colour=discord.Colour.greyple()
        )
        await ctx.send(embed=embed)

    @commands.command(aliases=['8ball'])
    async def _8ball(self, ctx, *, question):
        """
        This function is a command in a Python bot that uses the random module to provide a random response from a list of
        20 possible answers to a given question.

        :param ctx: ctx is the context object, which contains information about the command invocation. It includes
        attributes such as the message, the channel, the author, and more. It is used to interact with the Discord API and
        send messages, retrieve information, etc
        :param question: The `question` parameter is the question that the user wants to ask the 8-ball. It can be any
        string representing the question that the user wants an answer to
        """
        responses = ["It is certain.",
                     "It is decidedly so.",
                     "Without a doubt.",
                     "Yes - definitely.",
                     "You may rely on it.",
                     "As I see it, yes.",
                     "Most likely.",
                     "Outlook good.",
                     "Yes.",
                     "Signs point to yes.",
                     "Reply hazy, try again.",
                     "Ask again later.",
                     "Better not tell you now.",
                     "Cannot predict now.",
                     "Concentrate and ask again.",
                     "Don't count on it.",
                     "My reply is no.",
                     "My sources say no.",
                     "Outlook not so good.",
                     "Very doubtful."]
        await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

    @commands.command()
    async def ping(self, ctx):
        """
        The above function is a command in a Python Discord bot that calculates and sends the user's ping in milliseconds.

        :param ctx: ctx stands for "context" and it represents the context in which the command is being executed. It
        contains information about the message, the user who sent the message, the channel the message was sent in, and
        other relevant information
        """
        await ctx.send(f'Your ping is {round(self.client.latency * 1000)}ms')

    @commands.command()
    async def troll(self, ctx, user, amount=1):
        """
        The `troll` function sends a random message from a list of responses, mentioning a user, and deletes a specified
        number of messages in the channel.

        :param ctx: The `ctx` parameter stands for "context" and it represents the context in which the command is being
        invoked. It contains information about the message, the channel, the server, and the user who triggered the command
        :param user: The `user` parameter in the `troll` command represents the user you want to mention or refer to in the
        generated troll message. It is a required parameter, meaning you must provide a value for it when using the command
        :param amount: The `amount` parameter in the `troll` command is an optional parameter with a default value of 1. It
        specifies the number of messages to delete from the channel before sending the troll response. If no value is
        provided for `amount`, it will default to 1, defaults to 1 (optional)
        """
        if amount != 1:
            await ctx.send('Sorry that is invalid')
        responses = [f'Yo step bro can you help me {user} ?',
                     f'Help step bro Im stuck {user}!',
                     f'I need some help in the bathroom step bro {user}!',
                     f'What are you doing step bro {user}?']
        await ctx.channel.purge(limit=amount)
        await ctx.send(random.choice(responses))


async def setup(client):
    await client.add_cog(Commands(client))
