import os
import logging
import discord
from discord.utils import get
from discord.ext import commands
from dotenv import load_dotenv
from discord_components import DiscordComponents

import event_creation
import cal
import office_hours
import profanity
import qna
import db

logging.basicConfig(level=logging.INFO)


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
#GUILD = 'TeachersPet-Dev'
TESTING_MODE = None

intents=discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', description='This is TeachersPetBot!', intents=intents)

###########################
# Function: on_ready
# Description: run on bot start-up
###########################
@bot.event
async def on_ready():
    ''' run on bot start-up '''
    global TESTING_MODE
    TESTING_MODE = False

    DiscordComponents(bot)
    db.connect()
    db.mutation_query('''
        CREATE TABLE IF NOT EXISTS ta_office_hours (
            guild_id    INT,
            ta          VARCHAR(50),
            day         INT,
            begin_hr    INT,
            begin_min   INT,
            end_hr      INT,
            end_min     INT
        )
    ''')

    db.mutation_query('''
        CREATE TABLE IF NOT EXISTS exams (
            guild_id    INT,
            title       VARCHAR(50),
            desc        VARCHAR(300),
            date        VARCHAR(10),
            begin_hr    INT,
            begin_min   INT,
            end_hr      INT,
            end_min     INT
        )
    ''')

    db.mutation_query('''
        CREATE TABLE IF NOT EXISTS assignments (
            guild_id    INT,
            title       VARCHAR(50),
            link        VARCHAR(300),
            desc        VARCHAR(300),
            date        VARCHAR(10),
            due_hr      INT,
            due_min     INT
        )
    ''')

    event_creation.init(bot)
    office_hours.init(bot)
    await cal.init(bot)
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

###########################
# Function: on_guild_join
# Description: run when a user joins a guild with the bot present
# Inputs:
#      - guild: the guild the user joined from
###########################
@bot.event
async def on_guild_join(guild):
    ''' run on member joining guild '''
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send('Hi there, I\'m TeachersPetBot, and I\'m here' +
                'to help you manage your class discord! Let\'s do some quick setup.')
            #create roles if they don't exist
            if 'Instructor' in guild.roles:
                await channel.send("Instructor Role already exists")
            else:
                await guild.create_role(name="Instructor", colour=discord.Colour(0x0062ff),
                                        permissions=discord.Permissions.all())
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

###########################
# Function: on_message
# Description: run when a message is sent to a discord the bot occupies
# Inputs:
#      - message: the message the user sent to a channel
###########################
@bot.event
async def on_message(message):
    ''' run on message sent to a channel '''
    # allow messages from test bot
    if message.author.bot and message.author.id == 889697640411955251:
        ctx = await bot.get_context(message)
        await bot.invoke(ctx)

    if message.author == bot.user:
        return

    if profanity.check_profanity(message.content):
        await message.channel.send(message.author.name + ' says: ' +
            profanity.censor_profanity(message.content))
        await message.delete()

    await bot.process_commands(message)

    if message.content == 'hey bot':
        response = 'hey yourself ;)'
        await message.channel.send(response)

###########################
# Function: on_message_edit
# Description: run when a user edits a message
# Inputs:
#      - before: the old message
#      - after: the new message
###########################
@bot.event
async def on_message_edit(before, after):
    ''' run on message edited '''
    if profanity.check_profanity(after.content):
        await after.channel.send(after.author.name + ' says: ' +
            profanity.censor_profanity(after.content))
        await after.delete()

###########################
# Function: test
# Description: Simple test command that shows commands are working.
# Inputs:
#      - ctx: context of the command
# Outputs:
#      - Sends test successful message back to channel that called test
###########################
@bot.command()
async def test(ctx):
    ''' simple sanity check '''
    await ctx.send('test successful')

###########################
# Function: set_instructor
# Description: Command used to give Instructor role out by instructors
# Inputs:
#      - ctx: context of the command
#      - member: user to give role
# Outputs:
#      - Sends confirmation back to channel
###########################
@bot.command()
@commands.has_role('Instructor')
async def set_instructor(ctx, member:discord.Member):
    ''' set instructor role command '''
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
    ''' run event creation interface '''
    await event_creation.create_event(ctx, TESTING_MODE)

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
    ''' run office hour commands with various args '''
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
    ''' ask question command '''
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
    ''' answer question command '''
    # make sure to check that this is actually being asked in the Q&A channel
    if ctx.channel.name == 'q-and-a':
        await qna.answer(ctx, q_num, answer)
    else:
        await ctx.author.send('Please send answers to the #q-and-a channel.')
        await ctx.message.delete()

###########################
# Function: begin_tests
# Description: Start the automated testing
# Inputs:
#      - ctx: context of the command
###########################
@bot.command('begin-tests')
async def begin_tests(ctx):
    ''' start test command '''
    global TESTING_MODE

    if ctx.author.id != 889697640411955251:
        return

    TESTING_MODE = True

    test_oh_chan = next((ch for ch in ctx.guild.text_channels
        if 'office-hour-test' in ch.name), None)
    if test_oh_chan:
        await office_hours.close_oh(ctx.guild, 'test')

    await office_hours.open_oh(ctx.guild, 'test')

###########################
# Function: end_tests
# Description: Finalize automated testing
# Inputs:
#      - ctx: context of the command
###########################
@bot.command('end-tests')
async def end_tests(ctx):
    ''' end tests command '''
    if ctx.author.id != 889697640411955251:
        return

    await office_hours.close_oh(ctx.guild, 'test')

    # TODO maybe use ctx.bot.logout()
    await ctx.bot.close()
    # quit(0)

if __name__ == '__main__':
    bot.run(TOKEN)

###########################
# Function: test_dummy
# Description: Run the bot
###########################
def test_dummy():
    ''' run bot command '''
    bot.run(TOKEN)
