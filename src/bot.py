import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from discord_components import DiscordComponents, Button, ButtonStyle

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
client = discord.Client()

intents=discord.Intents.default()
bot = commands.Bot(command_prefix='!', description='This is TeachersPetBot!', intents=intents)
intents.members = True

@bot.event
async def on_ready():
    DiscordComponents(bot)
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


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

@bot.command('button')
async def button_command(ctx):
    await ctx.send("Content", components=[Button(style=ButtonStyle.blue, label="Blue"), Button(style=ButtonStyle.red, label="Red"), Button(style=ButtonStyle.URL, label="url", url="https://example.org")])
    while True:
        res = await bot.wait_for("button_click")
        await res.send(content=f'{res.component.label} clicked')

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