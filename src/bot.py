import os

from discord.ext import commands
from dotenv import load_dotenv

import init_server
import group_finding
import calendar
import office_hours
import profanity_filter
import qna



load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # profanity_filter.check_profanity(...args)

# office hour commands
@bot.command('oh')
@commands.has_role('admin')
async def office_hour_command():
    # office_hours.office_hour_command(args)
    pass

@bot.command('ask')
async def ask_question():
    # make sure to check that this is actually being asked in the Q&A channel
    # qna.ask(args)
    pass

@bot.command('answer')
async def answer_question():
    # make sure to check that this is actually being asked in the Q&A channel
    # qna.answer(args)
    pass

bot.run(TOKEN)