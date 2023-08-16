import discord
from discord.utils import get
from discord.ext import commands


class Admin(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['helpadmin'])
    @commands.has_permissions(administrator=True)
    async def helpAdmin(self, ctx):
        """
        The `helpAdmin` function sends an embedded message to the channel with a list of admin commands.

        :param ctx: The `ctx` parameter stands for "context" and it represents the context in which the command is being
        invoked. It contains information about the message, the channel, the server, and the user who triggered the command.
        It is an instance of the `commands.Context` class
        """
        embed = discord.Embed(
            title=":fire_extinguisher: Admin Commands",
            description="`kick`,`ban`,`unban`,`mute`,`unmute`,`clear`",
            colour=discord.Colour.red()
        )
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """
        This function allows a user with the "kick_members" permission to kick another member from the server and sends a
        message confirming the action.

        :param ctx: ctx is the context object, which contains information about the command being invoked, the message that
        triggered the command, the server and channel the command was used in, and more
        :param member: The "member" parameter is a required argument that represents the member you want to kick from the
        server. It should be a mention of the member (e.g., @username) or their ID
        :type member: discord.Member
        :param reason: The "reason" parameter is an optional argument that allows the person executing the command to
        provide a reason for kicking the member. This reason can be used to provide an explanation for the kick and can be
        accessed using the "reason" variable within the command
        """
        await ctx.send(f'User ' + member.display_name + ' has been Kicked.')
        await member.kick(reason=reason)

    @commands.command(pass_context=True)
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """
        This function bans a member from a Discord server and sends a message confirming the ban.

        :param ctx: ctx is the context object, which contains information about the command being invoked, the message that
        triggered the command, the server and channel it was sent in, and more
        :param member: The "member" parameter is a required argument that represents the member you want to ban from the
        server. It should be a mention of the member (e.g., @username) or their ID
        :type member: discord.Member
        :param reason: The "reason" parameter in the ban command is an optional parameter that allows the person executing
        the command to provide a reason for banning the member. This reason can be used to provide more context or
        justification for the ban. If no reason is provided, the value of the "reason" parameter will be
        """
        await ctx.send(f'User {member.display_name} has been banned.')
        await member.ban(reason=reason)

    @commands.command(pass_context=True)
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        """
        This is a Python function that allows a user with the "ban_members" permission to unban a member from the server.

        :param ctx: The `ctx` parameter stands for "context" and it represents the context in which the command is being
        invoked. It contains information about the message, the server, the channel, and the user who triggered the command
        :param member: The `member` parameter in the `unban` command is a string that represents the username and
        discriminator of the member to be unbanned. The format of the string should be `username#discriminator`. For
        example, if you want to unban a member with the username "JohnDoe
        """
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
        """
        This function mutes a specified member in a Discord server by assigning them the "Muted" role and setting
        permissions for that role in all channels.

        :param ctx: The `ctx` parameter stands for "context" and it represents the context in which the command is being
        invoked. It contains information about the message, the channel, the server, and the user who triggered the command
        :param member: The `member` parameter in the `mute` command is used to specify the member that you want to mute. It
        should be a mention of the member (e.g., `@username`) or their ID
        :type member: discord.Member
        :param reason: The `reason` parameter in the `mute` command is an optional parameter that allows the person muting
        the member to provide a reason for the mute. It can be any string value and is used to provide context or
        explanation for the mute action. If no reason is provided, it will default to
        """
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
        """
        This function unmutes a member by removing the "Muted" role from them in a Discord server.

        :param ctx: The `ctx` parameter stands for "context" and it represents the context in which the command is being
        invoked. It contains information about the message, the channel, the guild, the author, and more
        :param member: The `member` parameter in the `unmute` command is a required parameter of type `discord.Member`. It
        represents the member that you want to unmute
        :type member: discord.Member
        :param reason: The `reason` parameter is an optional argument that allows the person executing the command to
        provide a reason for unmuting the member. This can be useful for moderation purposes, as it provides a record of why
        the member was unmuted
        """
        guild = ctx.guild
        muted = get(guild.roles, name="Muted")
        await member.remove_roles(muted)
        await ctx.send(f'unmuted {member.mention}')

    @commands.command()
    async def clear(self, ctx, amount: int):
        """
        The above function is a command in a Python bot that clears a specified number of messages in a channel.

        :param ctx: ctx is the context object, which contains information about the command being executed, the message that
        triggered the command, the channel the command was executed in, the guild the command was executed in, and more. It
        is used to access and interact with various aspects of the Discord server
        :param amount: The "amount" parameter in the "clear" command is an integer that represents the number of messages to
        be cleared from the channel
        :type amount: int
        """
        if amount == 0:
            await ctx.send('Please pick a number that is not zero')
        await ctx.channel.purge(limit=amount)

    @clear.error
    async def clear_error(self, ctx, error):
        """
        The function `clear_error` handles the error when a required argument is missing and sends a message asking the user
        to specify the amount of messages to delete.

        :param ctx: The `ctx` parameter is an object that represents the context of the command being executed. It contains
        information such as the message that triggered the command, the channel it was sent in, the author of the message,
        and more
        :param error: The `error` parameter in the `clear_error` function is used to handle any errors that occur when the
        `clear` command is executed. Specifically, it checks if the error is an instance of
        `commands.MissingRequiredArgument`, which occurs when the user does not provide the required argument for the
        """
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please specify an amount of messages to delete.")

    @commands.has_permissions(kick_members=True)
    @commands.command()
    async def voiceKick(self, ctx, member: discord.Member):
        """
        The above function is a Discord bot command that kicks a member from a voice channel.

        :param ctx: ctx is the context object, which contains information about the command being invoked, such as the
        message, the channel, the guild, and the author. It is automatically passed to the command function when the command
        is called
        :param member: The `member` parameter in the `voiceKick` command is a required argument that expects a mention or
        the ID of a member in the server. This parameter represents the member that you want to kick from the voice channel
        they are currently in
        :type member: discord.Member
        """
        await ctx.send('Kicking ' + str(member))
        await member.move_to(None)
        await ctx.channel.purge(limit=2)


async def setup(client):
    await client.add_cog(Admin(client))
