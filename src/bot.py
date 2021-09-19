import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

import init_server
import group_finding
import cal
import office_hours
import profanity
import qna
import logging

logging.basicConfig(level=logging.INFO)


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
#GUILD = 'TeachersPet-Dev'

intents=discord.Intents.default()
bot = commands.Bot(command_prefix='!', description='This is TeachersPetBot!', intents=intents)
intents.members = True

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    office_hours.init(bot)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if(profanity.check_profanity(message.content)):
        await message.channel.send(message.author.name + ' says: ' + profanity.censor_profanity(message.content))
        await message.delete()

    await bot.process_commands(message)

    if message.content == 'hey bot':
        response = 'hey yourself'
        await message.channel.send(response)


'''
NOTE: bot commands don't work if client methods or bot on_message is implemented
'''
@bot.command()
async def test(ctx):
    await ctx.send('test successful')

# office hour commands
@bot.command(name='oh', help='Operations relevant for office hours.')
async def office_hour_command(ctx, command, *args):
    await office_hours.office_hour_command(ctx, command, *args)

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