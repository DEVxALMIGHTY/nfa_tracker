import discord
from discord.ext import commands

import json

with open('botsettings.json') as settings_file:
    settings = json.load(settings_file)

bot = commands.Bot(command_prefix=settings["prefix"], description=settings["description"])

# Remove default help command so we can customize
#bot.remove_command('help')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def metrics(ctx):
    await ctx.send("Show metrics ...")
   
bot.run(settings["token"])
