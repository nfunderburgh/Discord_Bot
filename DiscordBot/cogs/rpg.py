import json
import discord
import os
from discord.ext import commands

os.chdir(r'C:\Users\APR Services\PycharmProjects\bot')


class Rpg(commands.Cog):

    def __init__(self, client):
        self.client = client


'''
    @commands.Cog.listener()
    async def on_ready(self):
        with open('shop.json', 'r') as f:
            shop = json.load(f)

        with open('shop.json', 'w') as f:
            json.dump(shop, f)

    @commands.Cog.listener()
    async def on_member_join(self, ctx, member):
        with open('users.json', 'r') as f:
            users = json.load(f)

        await self.update_data(users, member)

        with open('users.json', 'w') as f:
            json.dump(users, f)

    @commands.Cog.listener()
    async def on_message(self, message):
        with open('users.json', 'r') as f:
            users = json.load(f)

        await self.update_data(users, message.author)
        await self.add_experience(users, message.author, 5)
        await self.addMoney(users, message.author, 5)
        await self.level_up(users, message.author, message.channel)

        with open('users.json', 'w') as f:
            json.dump(users, f)

    @commands.command()
    async def update_data(self, users, user):
        if str(user.id) in users or user.id == 760649572661592074:
            pass
        else:
            users[user.id] = {}
            users[user.id]['name'] = ''
            users[user.id]['experience'] = 0
            users[user.id]['level'] = 1
            users[user.id]['items'] = ''
            users[user.id]['money'] = 0

    @commands.command()
    async def name(self, ctx, newName):
        with open('users.json', 'r') as f:
            users = json.load(f)

        users[str(ctx.author.id)]['name'] = newName
        await ctx.send(f'Your name characters name is currently set to `{newName}`')

        with open('users.json', 'w') as f:
            json.dump(users, f)

    @commands.command()
    async def add_experience(self, users, user, exp):
        if str(user.id) in users:
            users[str(user.id)]['experience'] += exp

    @commands.command()
    async def level_up(self, users, user, channel):
        if str(user.id) in users:
            experience = users[str(user.id)]['experience']
            lvl_start = users[str(user.id)]['level']
            lvl_end = int(experience ** (1 / 4))

            if lvl_start < lvl_end:
                lvlup_cash = 2 ** lvl_end * 100
                await channel.send(
                    f'{user.mention} has leveled up to level {lvl_end} and {lvlup_cash} coins have been added to your account')
                users[str(user.id)]['level'] = lvl_end
                users[str(user.id)]['money'] += lvlup_cash
        else:
            pass

    @commands.command()
    async def addMoney(self, users, user, money):
        if str(user.id) in users:
            users[str(user.id)]['money'] += money

    @commands.command()
    async def shop(self, ctx):
        with open('shop.json', 'r') as f:
            shop = json.load(f)

        embed = discord.Embed(
            title="General Shop",
        )

        for name in shop:
            if shop[name]['quantity'] > 0:
                embed.add_field(name=shop[name]['emoji'] + "  " + shop[name]['items'],
                                value="price: `" + str(shop[name]['price']) + "`" + " coins" + "\nquantity: `" + str(
                                    shop[name]['quantity']) + "` left", inline=False)
            else:
                embed.add_field(name=shop[name]['emoji'] + "  " + shop[name]['items'], value="`Sold Out`", inline=False)

        await ctx.send(embed=embed)

        with open('shop.json', 'w') as f:
            json.dump(shop, f)

    @commands.command()
    async def buy(self, ctx, item):
        with open('shop.json', 'r') as f:
            shop = json.load(f)
        with open('users.json', 'r') as f:
            users = json.load(f)

        for name in shop:
            if shop[name]['items'].lower() == item.lower():
                if users[str(ctx.author.id)]['money'] >= shop[name]['price']:
                    if shop[name]['quantity'] > 0:
                        users[str(ctx.author.id)]['money'] = users[str(ctx.author.id)]['money'] - shop[name]['price']
                        shop[name]['quantity'] = shop[name]['quantity'] - 1
                        users[str(ctx.author.id)]['items'] = users[str(ctx.author.id)]['items'] + shop[name]['items']
                        await ctx.send("You have successfully bought a " + shop[name]['items'])
                else:
                    await ctx.send("You don't have enough money to buy " + shop[name]['items'])

        with open('users.json', 'w') as f:
            json.dump(users, f)
        with open('shop.json', 'w') as f:
            json.dump(shop, f)
'''


async def setup(client):
    await client.add_cog(Rpg(client))
