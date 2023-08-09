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
        embed = discord.Embed(
            title=":joy: Reddit Commands",
            description="`dogs`,`memes`,`cars`,`susmemes`",
            colour=discord.Colour.gold()
        )
        await ctx.send(embed=embed)

    @commands.command(pass_context=True, aliases=['car'])
    async def cars(self, ctx):
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
