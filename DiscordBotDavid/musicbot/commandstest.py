from discord.ext import commands

from musicbot import utils
import config

import run

import random
from collections import deque

class Tests(commands.Cog):
    """ A collection of the commands related to testing.
        Attributes:
            bot: The instance of the bot that is executing the commands.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='playlistcontent', description='Testing playlist content', help='Testing playlist content')
    async def _list_content(self, ctx):
        current_guild = utils.get_guild(self.bot, ctx.message)
        if current_guild is None:
            await utils.send_message(ctx, config.NO_GUILD_MESSAGE)
            return
        p_list = utils.guild_to_audiocontroller[current_guild].playlist  #get_deque()
        await ctx.send("```\n" + "Playlist Queue : " + str(p_list.playque) + "\n```")
        await ctx.send("```\n" + "Playlist History : " + str(p_list.playhistory) + "\n```")
        await ctx.send("```\n" + "Trackname History : " + str(p_list.trackname_history) + "\n```")

        #await utils.send_message(ctx, utils.guild_to_audiocontroller[current_guild].track_history())

    @commands.command(name='displayvolume', description='Testing volume', help='Testing volume')
    async def _display_volume(self, ctx):
        current_guild = utils.get_guild(self.bot, ctx.message)
        if current_guild is None:
            await utils.send_message(ctx, config.NO_GUILD_MESSAGE)
            return

        await ctx.send("```\n" + "Current Volume: " + str(utils.guild_to_audiocontroller[current_guild].volume) + "\n```")

    @commands.command(name='np', description='Displays current song playing', help='Displays current song playing')
    async def _current_song(self, ctx):
        current_guild = utils.get_guild(self.bot, ctx.message)
        if current_guild is None:
            await utils.send_message(ctx, config.NO_GUILD_MESSAGE)
            return
        songinfo = utils.guild_to_audiocontroller[current_guild].current_songinfo
        if songinfo is None:
            return
        await ctx.send(songinfo.output)
        #await ctx.message.author.send(songinfo.output)

    @commands.command(name='queue', description='Displays queue', help='Displays queue')
    async def _display_queue(self, ctx):
        current_guild = utils.get_guild(self.bot, ctx.message)
        if current_guild is None:
            await utils.send_message(ctx, config.NO_GUILD_MESSAGE)
            return
        p_list = utils.guild_to_audiocontroller[current_guild].playlist.playque  # get_deque()
        audiocontroller = utils.guild_to_audiocontroller[current_guild]
        await ctx.send("```\n" + "Upcoming Songs : \n```")
        pos = 0
        for url in p_list:
            title = audiocontroller.get_song_info(url)
            await ctx.send(str(pos) + ": " + title)
            pos += 1

        # await ctx.message.author.send(songinfo.output)

    @commands.command(name='clear', description='Clears all playlist information', help='Clears all playlist information')
    async def _clear(self, ctx):
        current_guild = utils.get_guild(self.bot, ctx.message)
        if current_guild is None:
            await utils.send_message(ctx, config.NO_GUILD_MESSAGE)
            return
        p_list = utils.guild_to_audiocontroller[current_guild].playlist  # get_deque()
        p_list.playque.clear()
        p_list.playhistory.clear()
        p_list.trackname_history.clear()
        await ctx.send("Queue has been cleared")
        # await ctx.message.author.send(songinfo.output)

    @commands.command(name='mv', description='Moves a song in the queue from a starting position to ending position',
                      help='Moves song from a to b')
    async def _move(self, ctx, old_pos, new_pos):
        current_guild = utils.get_guild(self.bot, ctx.message)
        if current_guild is None:
            await utils.send_message(ctx, config.NO_GUILD_MESSAGE)
            return
        p_list = utils.guild_to_audiocontroller[current_guild].playlist  # get_deque()
        url = p_list.playque.pop(old_pos)
        p_list.playque.insert(new_pos, url)
        await ctx.send("Moved song from position " + old_pos + " to position " + new_pos)

    @commands.command(name='ping', description='Returns the latency', help='Returns ping')
    async def ping(ctx):
        await ctx.send(f'{round(run.bot.latency * 1000)} ms')

    @commands.command(name='shuffle', description='Shuffles the queue', help='Shuffles queue')
    async def _shuffle(self, ctx):
        current_guild = utils.get_guild(self.bot, ctx.message)
        if current_guild is None:
            await utils.send_message(ctx, config.NO_GUILD_MESSAGE)
            return
        p_list = utils.guild_to_audiocontroller[current_guild].playlist
        queue = p_list.playque  # get_deque()
        new_queue = deque()
        length = queue.size()
        for i in range(length):
            num = random.randint(0, queue.size())
            url = queue.pop(num)
            new_queue.append(url)
        p_list.playque = new_queue

    @commands.command(name='queue', description='Loops the current song', help='Loops song')
    async def _loop(self, ctx):
        current_guild = utils.get_guild(self.bot, ctx.message)
        if current_guild is None:
            await utils.send_message(ctx, config.NO_GUILD_MESSAGE)
            return
        p_list = utils.guild_to_audiocontroller[current_guild].playlist.playque  # get_deque()
        audiocontroller = utils.guild_to_audiocontroller[current_guild]
        await ctx.send("```\n" + "Upcoming Songs : \n```")
        pos = 0
        for url in p_list:
            title = audiocontroller.get_song_info(url)
            await ctx.send(str(pos) + ": " + title)
            pos += 1

    @commands.command(name='seek', description='Loops the current song', help='Loops song')
    async def _seek(self, ctx):
        current_guild = utils.get_guild(self.bot, ctx.message)
        if current_guild is None:
            await utils.send_message(ctx, config.NO_GUILD_MESSAGE)
            return
        p_list = utils.guild_to_audiocontroller[current_guild].playlist.playque  # get_deque()
        audiocontroller = utils.guild_to_audiocontroller[current_guild]
        await ctx.send("```\n" + "Upcoming Songs : \n```")
        pos = 0
        for url in p_list:
            title = audiocontroller.get_song_info(url)
            await ctx.send(str(pos) + ": " + title)
            pos += 1

    #can also try implementing loopqueue

def setup(bot):
    bot.add_cog(Tests(bot))