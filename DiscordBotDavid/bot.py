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

load_dotenv('.env.txt')
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

#client = discord.Client()
status = cycle(['Status 1', 'Status2 2'])

bot = commands.Bot(command_prefix='!')

@bot.command(name='play', help='Connects bot to a voice channel')
async def play(ctx):
    if not ctx.message.author.voice:
        await ctx.send('You need to be connected to a voice channel.')
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()

@bot.command(name='stop', help='This command stops the bot.')
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
    # Change status of the bot!
    #await bot.change_presence(status=discord.Status.idle, activity=discord.Game('Hello there!'))
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
# client.run(TOKEN)