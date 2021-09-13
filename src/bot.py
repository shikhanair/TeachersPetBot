import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

import init_server
import group_finding
import calendar
import office_hours
import profanity_filter
import qna
import logging

logging.basicConfig(level=logging.INFO)


#load_dotenv()
#TOKEN = os.getenv('DISCORD_TOKEN')
TOKEN = ''
#GUILD = 'TeachersPet-Dev'
client = discord.Client()

'''
@client.event
async def on_ready():
    guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

client.run(TOKEN)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        await message.channel.send('Hello!')

client.run(TOKEN)
'''

intents=discord.Intents.default()
bot = commands.Bot(command_prefix='!', description='This is TeachersPetBot!', intents=intents)
intents.members = True

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

'''
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content == 'hey bot':
        response = 'hi user!!!'
        await message.channel.send(response)

    # profanity_filter.check_profanity(...args)
'''
'''
NOTE: bot commands don't work if client methods or bot on_message is implemented
'''
@bot.command()
async def test(ctx):
    await ctx.send('test successful')

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