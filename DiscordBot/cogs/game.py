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
        """
        The `helpGame` function sends an embedded message to the Discord channel with a title and description of game
        commands.

        :param ctx: The `ctx` parameter stands for "context" and it represents the context in which the command is being
        invoked. It contains information about the message, the channel, the server, and the user who triggered the command.
        It is an instance of the `commands.Context` class from the discord.py library
        """
        embed = discord.Embed(
            title=":game_die: Game Commands",
            description="`coinflip`,`fight`",
            colour=discord.Colour.red()
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def fight(self, ctx, member: discord.Member):
        """
        The `fight` function allows two users to engage in a turn-based fight, with each user having the option to hit or
        defend.

        :param ctx: The `ctx` parameter is an object that represents the context of the command being executed. It contains
        information such as the message, the channel, the author, and other relevant details
        :param member: The `member` parameter in the `fight` command is a required parameter of type `discord.Member`. It
        represents the member that the user wants to start a fight with
        :type member: discord.Member
        """
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
        """
        The function `printHit` sends a message to the context with information about a player hitting another player and
        the remaining hitpoints.

        :param ctx: The `ctx` parameter stands for "context" and represents the context in which the command is being
        invoked. It contains information about the message, the channel, the server, and the user who triggered the command
        :param playerHit: The player who performed the hit. It should be a mention of a user or a member object
        :param playerGetHit: The parameter "playerGetHit" represents the player who is getting hit. It is expected to be a
        mention of a user in the Discord server
        :param hit: The "hit" parameter represents the amount of hitpoints that the player has hit for
        :param hitpoints: The "hitpoints" parameter represents the remaining hitpoints of the player who got hit
        """
        await ctx.send(
            f'{playerHit.mention} has hit for {hit} hitpoints and {playerGetHit.mention} has {hitpoints} hitpoints left')

    @commands.command()
    async def coinflip(self, ctx, headsOrTails):
        """
        This function allows a user to play a coin flip game by guessing heads or tails and receiving a message indicating
        whether they won or lost.

        :param ctx: ctx is the context object, which contains information about the command being invoked, such as the
        message, the channel, the author, etc. It is used to send messages back to the user or the channel where the command
        was invoked
        :param headsOrTails: The `headsOrTails` parameter is a string that represents the user's choice of either "heads" or
        "tails"
        """
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
