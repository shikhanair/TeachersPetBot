import os
import discord
from discord.utils import get
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
    await cal.init(bot)
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send('Hi there, I\'m TeachersPetBot, and I\'m here to help you manage your class discord! Let\'s do some quick setup.')
            #create roles if they don't exist
            if 'Instructor' in guild.roles:
                await channel.send("Instructor Role already exists")
            else:
                await guild.create_role(name="Instructor", colour=discord.Colour(0x0062ff), permissions=discord.Permissions.all())
            #Assign Instructor role to admin
            leader = guild.owner
            leadrole = get(guild.roles, name='Instructor')
            await channel.send(leader.name + " has been given Instructor role!")
            await leader.add_roles(leadrole, reason=None, atomic=True)
            await channel.send("To assign more Instructors, type \"!setInstructor @<member>\"")
            #Create Text channels if they don't exist
            if 'instructor-commands' not in guild.text_channels:
                await guild.create_text_channel('instructor-commands')
                await channel.send("instructor-commands channel has been added!")
            if 'q-and-a' not in guild.text_channels:
                await guild.create_text_channel('q-and-a')
                await channel.send("q-and-a channel has been added!")
            if 'course-calendar' not in guild.text_channels:
                await guild.create_text_channel('course-calendar')
                await channel.send("course-calendar channel has been added!")

        break

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

@bot.command()
@commands.has_role('Instructor')
async def setInstructor(ctx, member:discord.Member):
    irole = get(ctx.guild.roles, name='Instructor')
    await member.add_roles(irole, reason=None, atomic=True)
    await ctx.channel.send(member.name + " has been given Instructor role!")

###########################
# Function: create_event
# Description: command to create event and send to event_creation module
# Ensures command author is Instructor
# Inputs:
#      - ctx: context of the command
# Outputs:
#      - Options to create event
###########################
@bot.command(name='create', help='Create a new event.')
# @commands.dm_only()
@commands.has_role('Instructor')
async def create_event(ctx):
    await event_creation.create_event(ctx)


###########################
# Function: oh
# Description: command related office hour and send to office_hours module
# Inputs:
#      - ctx: context of the command
#      - command: specific command to run
#      - *args: arguments for command
# Outputs:
#      - Office hour details and options
###########################
@bot.command(name='oh', help='Operations relevant for office hours.')
async def office_hour_command(ctx, command, *args):
    await office_hours.office_hour_command(ctx, command, *args)

###########################
# Function: ask
# Description: command to ask question and sends to qna module
# Inputs:
#      - ctx: context of the command
#      - question: question text
# Outputs:
#      - User question in new post
###########################
@bot.command(name='ask', help='Ask question. Please put question text in quotes.')
async def ask_question(ctx, question):
    # make sure to check that this is actually being asked in the Q&A channel
    if ctx.channel.name == 'q-and-a':
        await qna.question(ctx, question)
    else:
        await ctx.author.send('Please send questions to the #q-and-a channel.')
        await ctx.message.delete()


###########################
# Function: answer
# Description: command to answer question and sends to qna module
# Inputs:
#      - ctx: context of the command
#      - q_num: question number to answer
#      - answer: answer text
# Outputs:
#      - User answer in question post
###########################
@bot.command(name='answer', help='Answer specific question. Please put answer text in quotes.')
async def answer_question(ctx, q_num, answer):
    # make sure to check that this is actually being asked in the Q&A channel
    if ctx.channel.name == 'q-and-a':
        await qna.answer(ctx, q_num, answer)
    else:
        await ctx.author.send('Please send answers to the #q-and-a channel.')
        await ctx.message.delete()

bot.run(TOKEN)
