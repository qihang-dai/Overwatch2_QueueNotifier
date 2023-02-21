"""
Discord bot is not used in the final version of the project.
It is working, but its hard to find a way to deploy the bot on cloud 
while the program need to take screenshot from the local machine.
"""
from dotenv import load_dotenv
import os
import discord
import logging
import asyncio
from QueueWatcher import QueueWatcher
from sendMail import send
import re
import typing
import concurrent.futures

load_dotenv()
token = os.getenv('TOKEN')
guild_ids = os.getenv('GUILD_ID').split(',')

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot = discord.Bot()

qw = QueueWatcher()

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

@bot.slash_command(name = "hello", description = "Say hello to the bot")
async def hello(ctx):
    await ctx.respond("Hey!")

@bot.command(name = "queue", description = "Queue up for a game")
async def queue(ctx, email: typing.Optional[str]):
    # Get the author of the message (i.e., the user who triggered the command)
    author = ctx.author
    # Send a DM to the author
    await ctx.send(author.mention + "queue up")
    await author.send("You will receive a message when a game is found!", delete_after = 10)

    if email:
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_match = re.search(email_pattern, email)

    # Run the queue watcher in a separate thread using run_in_executor()
    loop = asyncio.get_running_loop()
    with concurrent.futures.ThreadPoolExecutor() as pool:
        found = await loop.run_in_executor(pool, qw.run)
    
    if found:
        await author.send("Game found!")
        await ctx.send(author.mention + "Game found!")
        if email_match:
            print("Sending email to %s", email)
            send(sender_email = None, password = None, receiver_email = email)

@bot.command(name = "stop", description = "Stop monitor the queue")
async def stop(ctx):
    # Get the author of the message (i.e., the user who triggered the command)
    author = ctx.author
    # Send a DM to the author
    await ctx.send(author.mention + "stop queue")
    await author.send("You will not receive a message when a game is found!", delete_after = 10)
    qw.stop()

#send a mention and dm to the user after 5 seconds
@bot.command()
async def test(ctx):
    # Get the author of the message (i.e., the user who triggered the command)
    author = ctx.author
    # Send a DM to the author
    await ctx.send(author.mention + "test")
    await author.send("You will receive a message in 5 seconds!", delete_after = 10)
    await asyncio.sleep(5)
    await author.send("Test successful!")
    await ctx.send(author.mention + "Test successful!")


bot.run(token)