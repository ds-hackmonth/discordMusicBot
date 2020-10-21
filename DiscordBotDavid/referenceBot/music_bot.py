import os
import discord
import random
import asyncio
import functools
import itertools

from discord.ext import commands, tasks
from dotenv import load_dotenv
from itertools import cycle

import youtube_dl
from async_timeout import timeout

#https://gist.github.com/vbe0201/ade9b80f2d3b64643d854938d40a0a2d

youtube_dl.utils.bug_reports_message = lambda: ''

class VoiceError(Exception):
    pass
class YTDLError(Exception):
    pass

class YTDLSource(discord.PCMVolumeTransformer):
    YTDL_OPTIONS = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0',
    }

    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn',
    }

    ytdl = youtube_dl.YoutubeDL(YTDL_OPTIONS)

    def __init__(self, ctx: commands.Context, source: discord.FFmpegPCMAudio, *, data: dict, volume: float = 0.5):
        super().__init__(source, volume)

        self.requester = ctx.author
        self.channel = ctx.channel
        self.data = data

        self.uploader = data.get('uploader')
        self.uploader_url = data.get('uploader_url')
        date = data.get('upload_date')
        self.upload_date = date[6:8] + '.' + date[4:6] + '.' + date[0:4]
        self.title = data.get('title')
        self.thumbnail = data.get('thumbnail')
        self.description = data.get('description')
        self.duration = self.parse_duration(int(data.get('duration')))
        self.tags = data.get('tags')
        self.url = data.get('webpage_url')
        self.views = data.get('view_count')
        self.likes = data.get('like_count')
        self.dislikes = data.get('dislike_count')
        self.stream_url = data.get('url')

    def __str__(self):
        return '**{0.title}** by **{0.uploader}**'.format(self)

    @classmethod
    async def create_source(cls, ctx: commands.Context, search: str, *, loop: asyncio.BaseEventLoop = None):
        loop = loop or asyncio.get_event_loop()

        partial = functools.partial(cls.ytdl.extract_info, search, download=False, process=False)
        data = await loop.run_in_executor(None, partial)

        if data is None:
            raise YTDLError('Couldn\'t find anything that matches `{}`'.format(search))

        if 'entries' not in data:
            process_info = data
        else:
            process_info = None
            for entry in data['entries']:
                if entry:
                    process_info = entry
                    break

            if process_info is None:
                raise YTDLError('Couldn\'t find anything that matches `{}`'.format(search))

        webpage_url = process_info['webpage_url']
        partial = functools.partial(cls.ytdl.extract_info, webpage_url, download=False)
        processed_info = await loop.run_in_executor(None, partial)

        if processed_info is None:
            raise YTDLError('Couldn\'t fetch `{}`'.format(webpage_url))

        if 'entries' not in processed_info:
            info = processed_info
        else:
            info = None
            while info is None:
                try:
                    info = processed_info['entries'].pop(0)
                except IndexError:
                    raise YTDLError('Couldn\'t retrieve any matches for `{}`'.format(webpage_url))

        return cls(ctx, discord.FFmpegPCMAudio(info['url'], **cls.FFMPEG_OPTIONS), data=info)

    @staticmethod
    def parse_duration(duration: int):
        minutes, seconds = divmod(duration, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        duration = []
        if days > 0:
            duration.append('{} days'.format(days))
        if hours > 0:
            duration.append('{} hours'.format(hours))
        if minutes > 0:
            duration.append('{} minutes'.format(minutes))
        if seconds > 0:
            duration.append('{} seconds'.format(seconds))

        return ', '.join(duration)

class Song:
    __slots__ = ('source', 'requester')
    def __init__(self, source: YTDLSource):
        self.source = source
        self.requester = source.requester
    def create_embed(self):
        embed = (discord.Embed(title='Now playing',
                               description='```css\n{0.source.title}\n```'.format(self),
                               color=discord.Color.blurple())
                 .add_field(name='Duration', value=self.source.duration)
                 .add_field(name='Requested by', value=self.requester.mention)
                 .add_field(name='Uploader', value='[{0.source.uploader}]({0.source.uploader_url})'.format(self))
                 .add_field(name='URL', value='[Click]({0.source.url})'.format(self))
                 .set_thumbnail(url=self.source.thumbnail))
        return embed

class SongQueue()

load_dotenv('.env.txt')
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

#client = discord.Client()
status = cycle(['Status 1', 'Status2 2'])

bot = commands.Bot(command_prefix='!')

@bot.command(name='play', help='Connects musicbot to a voice channel')
async def play(ctx):
    if not ctx.message.author.voice:
        await ctx.send('You need to be connected to a voice channel.')
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()

@bot.command(name='stop', help='This command stops the musicbot.')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    await voice_client.disconnect()

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Invalid command used.")
    #pass
    # if isinstance(error, commands.MissingRequiredArgument):
    #     await ctx.send("Please pass in required arguments.")

@bot.event
async def on_ready():
    # Change status of the musicbot!
    #await musicbot.change_presence(status=discord.Status.idle, activity=discord.Game('Hello there!'))
    change_status.start()
    print(f'{bot.user.name} has connected to Discord!')

@bot.event
async def on_member_join(member):
    print(f'{member} has joined the server! Welcome!')

@bot.event
async def on_member_remove(member):
    print(f'F - {member} has left the server')

@bot.command(help='returns the latency')
async def ping(ctx):
    await ctx.send(f'{round(bot.latency * 1000)} ms')

@bot.command(aliases=['8ball', 'test'])
async def _8ball(ctx, *, question):
    responses = ['your mom', 'your dad', 'your sister']
    await ctx.send(f'{random.choice(responses)}')

def is_it_me(ctx):
    return ctx.author.id == 1 #DISCORD USER ID HERE. Temporary holder

@bot.command()
@commands.has_permissions(manage_messages=True)
@commands.check(is_it_me)
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)
@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please specify amount of messages to delete.")

@bot.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)

@bot.command()
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)

@bot.command()
async def join(ctx):
    channel = ctx.message.author.voice.voice_channel
    await bot.join_voice_channel(channel)

@bot.command(name='create-channel')
@commands.has_role('admin')
async def create_channel(ctx, channel_name='real-python'):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)

@bot.command(name='roll_dice', help='Simulates rolling dice.')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.sned(', '.join(dice))

@tasks.loop(seconds=10)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))

bot.run(TOKEN)

# @client.event
# async def on_ready():
#     print(f'{client.user.name} has connected to Discord!')
#
# @client.event
# async def on_member_join(member):
#     await member.create_dm()
#     await member.dm_channel.send(
#         f"What's up {member.name}, welcome to my Discord server!"
#     )
#
# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return
#
#     brookyln_99_quotes = ['joe', 'mama']
#     if message.content == '99!':
#         response = random.choice(brookyln_99_quotes)
#         await message.channel.send(response)
#     elif message.content == 'raise-exception':
#         raise discord.DiscordException
#
# @client.event
# async def on_error(event, *args, **kwargs):
#     with open('err.log', 'a') as f:
#         if event == 'on_message':
#             f.write(f'Unhandled message: {args[0]}\n')
#         else:
#             raise
#     # #guild = discord.utils.find(lambda g : g.name == GUILD, client.guilds)
#     # guild = discord.utils.get(client.guilds, name=GUILD)
#     #
#     # # for guild in client.guilds:
#     # #     if guild.name == GUILD:
#     # #         break
#     #
#     # print(f'{client.user} is connected to the following guild:')
#     # print(f'{guild.name}(id: {guild.id})')
#     #
#     # print(guild.members)
#     # members = '\n - '.join([member.name for member in guild.members])
#     # print(f'Guild Members:\n - {members}')
#
