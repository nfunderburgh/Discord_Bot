import json
import asyncpraw
import praw
import random
import discord
from discord.ext import commands

# Author: Noah Funderburgh
# Date: 10/12/2020
# Description:
# Todo: Comment descriptions about each functions purpose, as well as parameters and return values.

with open('redditConfig.json') as f:
    data = json.load(f)
    client_id = data["client_id"]
    client_secret = data["client_secret"]
    username = data["username"]
    password = data["password"]
    user_agent = data["user_agent"]

reddit = asyncpraw.Reddit(client_id=client_id,
                          client_secret=client_secret,
                          username=username,
                          password=password,
                          user_agent=user_agent)


class Reddit(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(pass_contex=True, aliases=['helpreddit'])
    async def helpReddit(self, ctx):
        """
        The `helpReddit` function sends an embedded message to a Discord channel with a title and description of available
        Reddit commands.

        :param ctx: The `ctx` parameter stands for "context" and it represents the context in which the command is being
        executed. It contains information about the message, the channel, the server, and the user who triggered the
        command. It allows you to access and interact with various aspects of the Discord API
        """
        embed = discord.Embed(
            title=":joy: Reddit Commands",
            description="`dogs`,`memes`,`cars`,`susmemes`",
            colour=discord.Colour.gold()
        )
        await ctx.send(embed=embed)

    @commands.command(pass_context=True, aliases=['car'])
    async def cars(self, ctx):
        """
        This function retrieves a random car picture from the "carporn" subreddit and sends it as an embedded message in a
        Discord channel.

        :param ctx: The `ctx` parameter in the `cars` command represents the context of the command invocation. It contains
        information about the message, the channel, the server, and the user who triggered the command. It is passed
        automatically by the discord.py library when the command is invoked
        """
        submission = await reddit.subreddit("carporn")
        submission = random.choice([meme async for meme in submission.hot(limit=50)])
        embed = discord.Embed(
            title=submission.title,
            url=submission.url,
            colour=discord.Colour.blue()
        )
        embed.set_image(url=submission.url)
        embed.set_footer(text="Here is your car pic!")
        await ctx.send(embed=embed)

    @commands.command(pass_context=True, aliases=['cat'])
    async def cats(self, ctx):
        """
        This function retrieves a random cat picture from the "cats" subreddit and sends it as an embedded message in a
        Discord channel.

        :param ctx: The `ctx` parameter is the context object, which contains information about the command invocation. It
        includes attributes such as the message, the channel, the author, and more. It is used to interact with the Discord
        API and send messages or perform other actions related to the command
        """
        submission = await reddit.subreddit("cats")
        submission = random.choice([meme async for meme in submission.hot(limit=50)])
        embed = discord.Embed(
            title=submission.title,
            url=submission.url,
            colour=discord.Colour.blue()
        )
        embed.set_image(url=submission.url)
        embed.set_footer(text="Here is your dog pic!")
        await ctx.send(embed=embed)

    @commands.command(pass_context=True, aliases=['dog'])
    async def dogs(self, ctx):
        """
        This function retrieves a random dog picture from the "dogpictures" subreddit and sends it as an embedded message in
        a Discord channel.

        :param ctx: The `ctx` parameter is the context object, which contains information about the command invocation. It
        includes attributes such as the message, the channel, the author, and more
        """
        submission = await reddit.subreddit("dogpictures")
        submission = random.choice([meme async for meme in submission.hot(limit=50)])
        embed = discord.Embed(
            title=submission.title,
            url=submission.url,
            colour=discord.Colour.blue()
        )
        embed.set_image(url=submission.url)
        embed.set_footer(text="Here is your dog pic!")
        await ctx.send(embed=embed)

    @commands.command(pass_context=True, aliases=['meme'])
    async def memes(self, ctx):
        """
        The `memes` function retrieves a random meme from the "dankmemes" subreddit using the Reddit API, creates an embed
        with the meme's title and image, and sends it as a message in the current Discord channel.

        :param ctx: The `ctx` parameter is the context object, which contains information about the command invocation. It
        includes attributes such as the message, the channel, the author, and more. It is used to access information and
        perform actions related to the command
        """
        submission = await reddit.subreddit("dankmemes")
        submission = random.choice([meme async for meme in submission.hot(limit=100)])

        embed = discord.Embed(
            title=submission.title,
            url=submission.url,
            colour=discord.Colour.blue()
        )
        embed.set_image(url=submission.url)
        embed.set_footer(text="Here is your meme!")
        await ctx.send(embed=embed)

    @commands.command(pass_context=True, aliases=['susmeme'])
    async def susmemes(self, ctx):
        """
        The function retrieves a random "sus" meme from the "NSFWMemes" subreddit and sends it as an embedded message in a
        Discord channel.

        :param ctx: The `ctx` parameter in the `susmemes` command represents the context of the command invocation. It
        contains information about the message, the channel, the server, and the user who triggered the command. It is
        passed automatically by the discord.py library when the command is invoked
        """
        submission = await reddit.subreddit("NSFWMemes")
        submission = random.choice([meme async for meme in submission.hot(limit=50)])
        embed = discord.Embed(
            title=submission.title,
            url=submission.url,
            colour=discord.Colour.blue()
        )
        embed.set_image(url=submission.url)
        embed.set_footer(text="Here is your sus meme!")
        await ctx.send(embed=embed)


async def setup(client):
    await client.add_cog(Reddit(client))
