import discord
import shutil
import youtube_dl
import os
from discord.utils import get
from discord.ext import commands

queues = {}


# Author: Noah Funderburgh
# Date: 10/9/2020
# Description:
# Todo: Comment descriptions about each functions purpose, as well as parameters and return values.


class Music(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command(pass_contex=True, aliases=['helpmusic'])
    async def helpMusic(self, ctx):
        """
        The `helpMusic` function sends an embedded message containing a list of music commands to the Discord channel.

        :param ctx: The `ctx` parameter is the context object that contains information about the command invocation. It
        includes attributes such as the message, the channel, the author, and more. It is used to interact with the Discord
        API and send messages, embeds, etc
        """
        embed = discord.Embed(
            title=":musical_note: Music Commands",
            description="`join`,`play`,`pause`,`resume`,`stop`,`queue`,`leave`",
            colour=discord.Colour.blue()
        )
        await ctx.send(embed=embed)


    @commands.command(pass_context=True)
    async def join(self, ctx):
        """
        The `join` function allows the bot to join the voice channel of the user who invoked the command.

        :param ctx: ctx is short for "context" and it represents the context in which the command is being executed. It
        contains information about the message, the author, the server, and other relevant details
        """
        channel = ctx.author.voice.channel
        await channel.connect()

    @commands.command(pass_context=True, aliases=['p', 'pla'])
    async def play(self, ctx, url: str):
        """
        The `play` function in this Python code downloads and plays audio from a given URL, and also handles queuing of
        songs.

        :param ctx: The `ctx` parameter is the context object, which contains information about the command invocation such
        as the message, the channel, the guild, and the author
        :param url: The `url` parameter is a string that represents the URL of the audio or video that you want to play. It
        is used to download the audio from the given URL and play it
        :type url: str
        :return: The function `play` does not have a return statement, so it does not explicitly return anything.
        """
        global name

        def check_queue():
            Queue_infile = os.path.isdir("./Queue")
            if Queue_infile is True:
                DIR = os.path.abspath(os.path.realpath("./Queue"))
                length = len(os.listdir(DIR))
                still_q = length - 1
                try:
                    first_file = os.listdir(DIR)[0]
                except:
                    print("No more queued song(s)\n")
                    queues.clear()
                    return
                main_location = os.path.dirname(os.path.realpath("./music.py"))
                song_path = os.path.abspath(os.path.realpath("Queue") + "\\" + first_file)
                if length != 0:
                    print("Song done, playing next queued\n")
                    print(f"Songs still in queue: {still_q}")
                    song_there = os.path.isfile("song.mp3")
                    if song_there:
                        os.remove("song.mp3")
                    shutil.move(song_path, main_location)
                    for file in os.listdir("./"):
                        if file.endswith(".mp3"):
                            os.rename(file, 'song.mp3')

                    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
                    voice.source = discord.PCMVolumeTransformer(voice.source)
                    voice.source.volume = 0.07
                else:
                    queues.clear()
                    return
            else:
                queues.clear()
                print("No songs were queued before the ending of the last song\n")

        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
                queues.clear()
                print("Removed old song file")
        except PermissionError:
            print("Trying to delete song file, but it's being played")
            await ctx.send("ERROR: Music playing")
            return

        Queue_infile = os.path.isdir("./Queue")
        try:
            Queue_folder = "./Queue"
            if Queue_infile is True:
                print("Removed old Queue Folder")
                shutil.rmtree(Queue_folder)
        except:
            print("No old Queue folder")

        await ctx.send("Getting everything ready now")

        voice = get(self.client.voice_clients, guild=ctx.guild)

        ydl_opts = {
            'format': 'bestaudio/best',
            # 'quiet': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Downloading audio now\n")
            ydl.download([url])

        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                name = file
                print(f"Renamed File: {file}\n")
                os.rename(file, "song.mp3")

        voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.07
        nname = name.rsplit("-", 2)
        await ctx.send(f"Playing: {nname[0]}")
        print("playing\n")

    @commands.command(pass_context=True, aliases=['pa', 'pau'])
    async def pause(self, ctx):
        """
        This function pauses the currently playing music in a voice channel.

        :param ctx: ctx is the context object, which contains information about the command being invoked, such as the
        message, the author, the guild, etc. It is passed as the first parameter to the command function
        """
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_playing():
            print("Music paused")
            voice.pause()
            await ctx.send("Music paused")
        else:
            print("Music not playing failed pause")
            await ctx.send("Music not playing failed pause")

    @commands.command(pass_context=True, aliases=['r', 'res'])
    async def resume(self, ctx):
        """
        The `resume` function resumes the paused music if it is currently paused, otherwise it sends a message indicating
        that the music is not paused.

        :param ctx: The `ctx` parameter is the context object, which contains information about the command invocation. It
        includes attributes such as the message, the author, the channel, and the guild where the command was invoked. In
        this case, `ctx.guild` is used to get the guild (server) where the
        """
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_paused():
            print("Resumed music")
            voice.resume()
            await ctx.send("Resumed music")
        else:
            print("Music is not paused")
            await ctx.send("Music is not paused")

    @commands.command(pass_context=True, aliases=['s', 'sto', 'skip'])
    async def stop(self, ctx):
        """
        The `stop` function stops the currently playing music and clears the music queue.

        :param ctx: The `ctx` parameter is the context object, which contains information about the command invocation such
        as the message, the channel, the guild, and the author. It is passed automatically by the discord.py library when
        the command is invoked
        """
        voice = get(self.client.voice_clients, guild=ctx.guild)

        queues.clear()

        if voice and voice.is_playing():
            print("Music stopped")
            voice.stop()
            await ctx.send("Music stopped")
        else:
            print("No music playing failed to stop")
            await ctx.send("No music playing failed to stop")

    @commands.command(pass_context=True, aliases=['q', 'que'])
    async def queue(self, ctx, url: str):
        """
        The `queue` function downloads an audio file from a given URL and adds it to a queue.

        :param ctx: ctx is the context object, which contains information about the command invocation such as the message,
        the channel, the author, etc. It is used to interact with the Discord API and send messages, perform actions, etc
        :param url: The `url` parameter is a string that represents the URL of the YouTube video that you want to add to the
        queue
        :type url: str
        """
        Queue_infile = os.path.isdir("./Queue")
        if Queue_infile is False:
            os.mkdir("Queue")
        DIR = os.path.abspath(os.path.realpath("Queue"))
        q_num = len(os.listdir(DIR))
        q_num += 1
        add_queue = True
        while add_queue:
            if q_num in queues:
                q_num += 1
            else:
                add_queue = False
                queues[q_num] = q_num

        queue_path = os.path.abspath(os.path.realpath("Queue") + f"\song{q_num}.%(ext)s")

        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'outtmpl': queue_path,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '100',
            }],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Downloading audio now\n")
            ydl.download([url])
        await ctx.send("Adding song " + str(q_num) + " to the queue")

        print("Song added to queue\n")

    @commands.command(pass_contex=True)
    async def leave(self, ctx):
        """
        The above function is a command in a Python Discord bot that disconnects the bot from the voice channel it is
        currently in.

        :param ctx: ctx stands for "context" and it represents the context in which the command is being executed. It
        contains information about the message, the channel, the server, and the user who triggered the command
        """
        await ctx.voice_client.disconnect()


async def setup(client):
    await client.add_cog(Music(client))
