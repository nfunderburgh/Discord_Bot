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
        await self.client.change_presence(status=discord.Status.do_not_disturb,
                                          activity=discord.Game('with my step bro'))
        print('Bot is ready.')

    @commands.command()
    async def help(self, ctx):
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
        embed = discord.Embed(
            title=":tools: Utility Commands",
            description="`8ball`,`ping`,`troll`",
            colour=discord.Colour.greyple()
        )
        await ctx.send(embed=embed)

    @commands.command(aliases=['8ball'])
    async def _8ball(self, ctx, *, question):
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
        await ctx.send(f'Your ping is {round(self.client.latency * 1000)}ms')

    @commands.command()
    async def troll(self, ctx, user, amount=1):
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
