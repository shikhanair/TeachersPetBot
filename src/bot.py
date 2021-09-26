import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from discord_components import DiscordComponents, Button, ButtonStyle

import init_server
import event_creation
import cal
import office_hours
import profanity
import qna
import logging
import db

logging.basicConfig(level=logging.INFO)


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
#GUILD = 'TeachersPet-Dev'

intents=discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', description='This is TeachersPetBot!', intents=intents)


@bot.event
async def on_ready():
    DiscordComponents(bot)
    db.connect()
    event_creation.init(bot)
    office_hours.init(bot)
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
        response = 'hey yourself ;)'
        await message.channel.send(response)

@bot.event
async def on_message_edit(before, after):
    if profanity.check_profanity(after.content):
        await after.channel.send(after.author.name + ' says: ' + profanity.censor_profanity(after.content))
        await after.delete()


@bot.command()
async def test(ctx):
    await ctx.send('test successful')

@bot.command(name='create', help='Create a new event.')
# @commands.dm_only()
@commands.has_role('Instructor')
async def create_event(ctx):
    await event_creation.create_event(ctx)

# office hour commands
@bot.command(name='oh', help='Operations relevant for office hours.')
async def office_hour_command(ctx, command, *args):
    await office_hours.office_hour_command(ctx, command, *args)



@bot.command('ask')
async def ask_question(ctx, question):
    # make sure to check that this is actually being asked in the Q&A channel
    if ctx.channel.name == 'q-and-a':
        await qna.question(ctx, question)
    else:
        await ctx.author.send('Please send questions to the #q-and-a channel.')
        await ctx.message.delete()

#`````````````````````````````````````````````````````````````````````````````
#calendar commands
@bot.command('calendar')
async def calendar(ctx):
    if ctx.channel.name == 'calendar':
        await ctx.send("Here\'s what it\'s going to look like, sire", components=[Button(label="Click to View", custom_id="button1")])
        interaction = await bot.wait_for("button_click", check=lambda inter: inter.custom_id == "button1")
        await interaction.send(content="C A L E N D A R")
    else:
        await ctx.author.send('Please use the #calendar channel!')
        await ctx.message.delete()




#`````````````````````````````````````````````````````````````````````````````


@bot.command('answer')
async def answer_question(ctx, q_num, answer):
    # make sure to check that this is actually being asked in the Q&A channel
    if ctx.channel.name == 'q-and-a':
        await qna.answer(ctx, q_num, answer)
    else:
        await ctx.author.send('Please send answers to the #q-and-a channel.')
        await ctx.message.delete()

bot.run(TOKEN)
