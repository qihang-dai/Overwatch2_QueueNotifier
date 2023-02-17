from dotenv import load_dotenv
import os
import discord
import logging

load_dotenv()
token = os.getenv('TOKEN')
guild_ids = os.getenv('GUILD_ID').split(',')

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

@bot.slash_command(name = "hello", description = "Say hello to the bot")
async def hello(ctx):
    await ctx.respond("Hey!")

@bot.command()
async def queue(ctx, description = "send you a message when game is found"):
    # Get the author of the message (i.e., the user who triggered the command)
    author = ctx.author
    # Send a DM to the author
    await author.send("You will receive a message when a game is found!", delete_after = 10)

    #TODO: start the queue watcher

bot.run(token)