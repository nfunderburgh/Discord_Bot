import discord
from discord.utils import get
from discord.ext import commands


class Admin(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Custom help message for the admin class so there isn't a long list of commands
    # Verifies the user has admin permissions to use command
    #
    # param: self, represents an instance of the class
    # param: ctx, represents the context in which a command is being invoked under
    @commands.command(aliases=['helpadmin'])
    @commands.has_permissions(administrator=True)
    async def helpAdmin(self, ctx):
        embed = discord.Embed(
            title=":fire_extinguisher: Admin Commands",
            description="`kick`,`ban`,`unban`,`mute`,`unmute`,`clear`",
            colour=discord.Colour.red()
        )
        await ctx.send(embed=embed)

    # Kicks the user from the server
    # Verifies the user has kicking permissions to use command
    #
    # param: self, represents an instance of the class
    # param: ctx, represents the context in which a command is being invoked under
    # param: member, the member to kick from the server
    # param: reason, the reason why the member was kick if nothing is type there will be none
    @commands.command(pass_context=True)
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await ctx.send(f'User ' + member.display_name + ' has been Kicked.')
        await member.kick(reason=reason)

    @commands.command(pass_context=True)
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await ctx.send(f'User {member.display_name} has been banned.')
        await member.ban(reason=reason)

    @commands.command(pass_context=True)
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_user = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_user:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {user.name}#{user.discriminator}')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        guild = ctx.guild
        muted = get(guild.roles, name="Muted")
        if not muted:
            muted = await guild.create_role(name="Muted")

            for channel in guild.channels:
                await channel.set_permissions(muted, speak=False, send_messages=False, read_message_history=True,
                                              read_messages=True)
        await member.add_roles(muted)
        await ctx.send(f"Muted{member.mention} for {reason}")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, member: discord.Member, *, reason=None):
        guild = ctx.guild
        muted = get(guild.roles, name="Muted")
        await member.remove_roles(muted)
        await ctx.send(f'unmuted {member.mention}')

    @commands.command()
    async def clear(self, ctx, amount: int):
        if amount == 0:
            await ctx.send('Please pick a number that is not zero')
        await ctx.channel.purge(limit=amount)

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please specify an amount of messages to delete.")

    # Kicks the user from the voice char
    # Verifies the user has kicking permissions to use command
    #
    # param: self, represents an instance of the class
    # param: ctx, represents the context in which a command is being invoked under
    # param: member, the member to kick from the voice chat
    @commands.has_permissions(kick_members=True)
    @commands.command()
    async def voiceKick(self, ctx, member: discord.Member):
        await ctx.send('Kicking ' + str(member))
        await member.move_to(None)
        await ctx.channel.purge(limit=2)


async def setup(client):
    await client.add_cog(Admin(client))
