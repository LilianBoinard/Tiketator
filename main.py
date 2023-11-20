import discord
from discord.ext import commands

from dotenv import load_dotenv
import os

import CogTickets

# ------------- env variables --------------
load_dotenv()
token = str(os.getenv('token'))
error_channel = int(os.getenv('error_channel'))
description = str(os.getenv('description'))
# ------------------------------------------

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='/', description=description, intents=intents)


# ---------- Events -----------
@bot.event
async def on_ready():
    await bot.add_cog(CogTickets.CogTickets(bot))
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('traiter vos tickets'))
    print('Tiketator Ready !')


@bot.event
async def on_message(message):
    # don't respond to ourselves
    if message.author == bot.user:
        return

    await bot.process_commands(message)

    if not isinstance(message.channel, discord.channel.DMChannel):
        if '/tickets' in message.content:
            await message.delete()


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.author.send("Il manque un/des argument(s).")
    else:
        await bot.get_channel(error_channel).send(error)


# -----------------------------

bot.run(token)
