#!/usr/bin/env python3
import os
import discord
from discord.ext import commands
import yaml

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
ENABLED_COGS = [
    'git-notifier.py'
]

bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))

@bot.command(description='Get bot latency (useful for testing upstate of the bot')
async def ping(ctx):
    await ctx.send(f'Ping! {round(bot.latency * 1000)}ms')

# load all the cogs
for filename in os.listdir(os.path.join(ROOT_DIR, 'cogs')):
    if filename in ENABLED_COGS:
        print(f'Loading cog: {filename}')
        bot.load_extension(f'cogs.{filename[:-3]}')

# run bot with token
bot.run(os.environ.get("DISCORD_BOT_TOKEN"))

