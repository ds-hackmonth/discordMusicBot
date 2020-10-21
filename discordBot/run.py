import discord
from discord.ext import commands

#import config
from config import *
from referenceBot.audiocontroller import AudioController
from referenceBot.utils import guild_to_audiocontroller

#initial_extensions = ['musicbot.commands.music', 'musicbot.commands.general']
initial_extensions = ['referenceBot.commandsmusic', 'referenceBot.commandsgeneral', 'referenceBot.commandstest']
bot = commands.Bot(command_prefix="!", pm_help=True)

if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(e)


@bot.event
async def on_ready():
    print(STARTUP_MESSAGE)
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name=" Music, type !help "))

    for guild in bot.guilds:
        print(guild.name)
        await guild.me.edit(nick=DEFAULT_NICKNAME)
        guild_to_audiocontroller[guild] = AudioController(bot, guild, DEFAULT_VOLUME)
        try:
            await guild_to_audiocontroller[guild].register_voice_channel(guild.voice_channels[0])
        except Exception as e:
            print("could not join " + guild.name + "\n" + str(e))

    print(STARTUP_COMPLETE_MESSAGE)


@bot.event
async def on_guild_join(guild):
    print(guild.name)
    guild_to_audiocontroller[guild] = AudioController(bot, guild, DEFAULT_VOLUME)
    try:
        await guild_to_audiocontroller[guild].register_voice_channel(guild.voice_channels[0])
    except:
        print("could not join " + guild.name)


bot.run(token, bot=True, reconnect=True)