from discord.ext import commands

from musicbot import utils
import config

class Tests(commands.Cog):
    """ A collection of the commands related to music playback.
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

    # @commands.command(name='queue', description='Displays queue', help='Displays queue')
    # async def _display_queue(self, ctx):
    #     current_guild = utils.get_guild(self.bot, ctx.message)
    #     if current_guild is None:
    #         await utils.send_message(ctx, config.NO_GUILD_MESSAGE)
    #         return
    #     p_list = utils.guild_to_audiocontroller[current_guild].playlist.playque  # get_deque()
    #     for url in p_list:
    #
    #
    #
    #
    #     await ctx.send("```\n" + "Upcoming Songs : " + str(p_list.playque_titles) + "\n```")
    #     # await ctx.message.author.send(songinfo.output)

def setup(bot):
    bot.add_cog(Tests(bot))