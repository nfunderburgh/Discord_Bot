import discord
import asyncio
import random

from discord.ext import commands


# Author: Noah Funderburgh
# Date: 10/8/2020
# Description:
# Todo: Comment descriptions about each functions purpose, as well as parameters and return values.

class Game(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['helpgame'])
    async def helpGame(self, ctx):
        embed = discord.Embed(
            title=":game_die: Game Commands",
            description="`coinflip`,`fight`",
            colour=discord.Colour.red()
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def fight(self, ctx, member: discord.Member):

        await ctx.send(
            f'{ctx.author.mention} is trying to start a fight with you {member.mention} will you `accept` or `decline`?')

        try:
            msg = await self.client.wait_for(
                "message",
                timeout=60,
                check=lambda message: message.author == member and message.channel == ctx.channel
            )
            if msg.content == 'accept':
                await ctx.send(f'{member.mention} has decided to accept the fight')
            else:
                await ctx.send(f'{member.mention}they chickend out')

            if msg.content == 'accept':
                hitpointsPlayerOne = 100
                hitpointsPlayerTwo = 100
                count = 0
                while hitpointsPlayerOne > 0 and hitpointsPlayerTwo > 0:
                    count = count + 1
                    if count % 2 == 1:
                        user = member
                    else:
                        user = ctx.author
                    await ctx.send(f'{user.mention} will you `hit` or `defend`?')
                    try:
                        msg = await self.client.wait_for(
                            "message",
                            timeout=60,
                            check=lambda message: message.author == user and message.channel == ctx.channel
                        )
                        if msg.content == 'defend':
                            hit = random.randint(1, 20)
                            if count % 2 == 1:
                                hitpointsPlayerTwo = hitpointsPlayerTwo - hit
                                await ctx.send(
                                    f'{user.mention} has hit for {hit} hitpoints and {ctx.author.mention} has {hitpointsPlayerTwo} hitpoints left')
                            else:
                                hitpointsPlayerOne = hitpointsPlayerOne - hit
                                await ctx.send(
                                    f'{user.mention} has hit for {hit} hitpoints and {member.mention} has {hitpointsPlayerOne} hitpoints left')

                        if msg.content == 'hit':
                            hit = random.randint(1, 40)
                            if count % 2 == 1:
                                hitpointsPlayerTwo = hitpointsPlayerTwo - hit
                                await self.printHit(ctx, user, ctx.author, hit, hitpointsPlayerTwo)
                            else:
                                hitpointsPlayerOne = hitpointsPlayerOne - hit
                                await self.printHit(ctx, user, member, hit, hitpointsPlayerOne)
                    except asyncio.TimeoutError:
                        await ctx.send(f'{user.mention} has not responded.', delete_after=10)
                if hitpointsPlayerTwo < 0:
                    await ctx.send(f'{member.mention} has won the fight!')
                else:
                    await ctx.send(f'{ctx.author.mention} has won the fight!')
        except asyncio.TimeoutError:
            await ctx.send(f'{member.mention} has not responded.', delete_after=10)

    @commands.command()
    async def printHit(self, ctx, playerHit, playerGetHit, hit, hitpoints):
        await ctx.send(
            f'{playerHit.mention} has hit for {hit} hitpoints and {playerGetHit.mention} has {hitpoints} hitpoints left')

    @commands.command()
    async def coinflip(self, ctx, headsOrTails):
        coin = random.randint(0, 1)
        headsOrTails = headsOrTails.lower()
        if headsOrTails == 'tails':
            if coin == 0:
                await ctx.send('You won the coin was tails!')
            else:
                await ctx.send('You lost the coin was heads')
        elif headsOrTails == 'heads':
            if coin == 1:
                await ctx.send('You won the coin was heads')
                await ctx.send('You won the coin was heads')
            else:
                await ctx.send('You lost the coin was tails')
        else:
            await ctx.send('Invalid argument please pick either heads or tails')


async def setup(client):
    await client.add_cog(Game(client))
