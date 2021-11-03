import platform
import asyncio
import os
from time import time
from platform import python_version
from datetime import datetime, timedelta
from psutil import Process, virtual_memory
from apscheduler.schedulers.asyncio import AsyncIOScheduler


import discord
from discord import Embed
from discord.ext import commands
from discord.utils import get
from discord import __version__ as discord_version
from discord_components import DiscordComponents

from dotenv import load_dotenv



import db
import profanity
import event_creation
import office_hours
import cal
import qna

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'

numbers = ("1️⃣", "2⃣", "3⃣", "4⃣", "5⃣",
		   "6⃣", "7⃣", "8⃣", "9⃣", "🔟")

if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
print(TOKEN)
BOT_VERSION=os.getenv('VERSION')
print(BOT_VERSION)
Test_bot_application_ID = int(os.getenv('TEST_BOT_APP_ID'))

TESTING_MODE = None

intents=discord.Intents.all()
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
            day         VARCHAR(4),
            begin_time  DATETIME,
            end_time    DATETIME
        )
    ''')

    db.mutation_query('''
        CREATE TABLE IF NOT EXISTS exams (
            guild_id    INT,
            title       VARCHAR(50),
            desc        VARCHAR(300),
            duration    VARCHAR(15),
            begin_date  DATETIME,
            end_date    DATETIME
        )
    ''')

    db.mutation_query('''
        CREATE TABLE IF NOT EXISTS assignments (
            guild_id    INT,
            title       VARCHAR(50),
            link        VARCHAR(300),
            desc        VARCHAR(300),
            date        DATETIME
        )
    ''')

    db.mutation_query('''
        CREATE TABLE IF NOT EXISTS qna (
            guild_id    INT,
            author       VARCHAR(50),
            answer        VARCHAR(300),
            qnumber      INT
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
# Description: run when a the bot joins a guild
# Inputs:
#      - guild: the guild the user joined from
###########################
@bot.event
async def on_guild_join(guild):
    ''' run on member joining guild '''
    channel = get(guild.text_channels, name='general')
    if channel is None:
        await guild.create_text_channel('general')
        channel = get(guild.text_channels, name='general')
    if channel.permissions_for(guild.me).send_messages:
        await channel.send('Hi there, I\'m TeachersPetBot, and I\'m here' +
            'to help you manage your class discord! Let\'s do some quick setup.')
        await guild.create_role(name="Instructor", colour=discord.Colour(0x0062ff),
                                    permissions=discord.Permissions.all())
        leadrole = get(guild.roles, name='Instructor')
         #Assign Instructor role to admin is there is no Instructor
        if len(leadrole.members) == 0:
            leader = guild.owner
            leadrole = get(guild.roles, name='Instructor')
            await channel.send(leader.name + " has been given Instructor role!")
            await leader.add_roles(leadrole, reason=None, atomic=True)
        else:
            for member in leadrole.members:
                await member.add_roles(leadrole, reason=None, atomic=True)
            instructors = ", ".join([str(x).rsplit("#", 1)[0] for x in leadrole.members])
            if len(leadrole.members) == 1:
                await channel.send(instructors + " is the Instructor!")
            else:
                await channel.send(instructors + " are the Instructors!")
        await channel.send("To add Instructors, type \"!setInstructor @<member>\"")
        #await channel.send("To remove instructors, type \"!removeInstructor @<member>\"")
        #Create Text channels if they don't exist
        overwrites = {guild.default_role: discord.PermissionOverwrite(read_messages=False,
            send_messages=False), leadrole: discord.PermissionOverwrite(read_messages=True,
            send_messages=True)}
        if get(guild.text_channels, name='instructor-commands') is None:
            await guild.create_text_channel('instructor-commands', overwrites=overwrites)
            await channel.send("instructor-commands channel has been added!")
        else:
            await channel.send("instructor-commands channel is already present!")
        if get(guild.text_channels, name='q-and-a') is None:
            await guild.create_text_channel('q-and-a')
            await channel.send("q-and-a channel has been added!")
        else:
            await channel.send("q-and-a channel is already present!")
        if get(guild.text_channels, name='course-calendar') is None:
            await guild.create_text_channel('course-calendar')
            await channel.send("course-calendar channel has been added!")
        else:
            await channel.send("course-calendar channel is already present!")

###########################
# Function: on_member_join
# Description: run when member joins a guild in which bot is alreay present
# Inputs:
#      - member: the user details
###########################
@bot.event
async def on_member_join(member):
    channel = get(member.guild.text_channels, name='general')
    await channel.send(f"Hello {member}!")
    await member.send(f'You have joined {member.guild.name}!')

###########################
# Function: on_member_remove
# Description: run when member leaves a guild in which bot is alreay present
# Inputs:
#      - guild: the guild the user joined from
###########################
@bot.event
async def on_member_remove(member):
    channel = get(member.guild.text_channels, name='general')
    await channel.send(f"{member.name} has left")

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
    if message.author.bot and message.author.id == Test_bot_application_ID:
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
# Function: get_instructor
# Description: Command used to give Instructor role out by instructors
# Inputs:
#      - ctx: context of the command
#      - member: user to give role
# Outputs:
#      - Sends confirmation back to channel
###########################
@bot.command(name='getInstructor', help='Find Instructors')
async def get_instructor(ctx):
    ''' set instructor role command '''
    leadrole = get(ctx.guild.roles, name='Instructor')
    instructors = ", ".join([str(x).rsplit("#", 1)[0] for x in leadrole.members])
    if len(leadrole.members) == 1:
        await ctx.send(instructors + " is the Instructor!")
    else:
        await ctx.send(instructors + " are the Instructors!")

###########################
# Function: set_instructor
# Description: Command used to give Instructor role out by instructors
# Inputs:
#      - ctx: context of the command
#      - member: user to give role
# Outputs:
#      - Sends confirmation back to channel
###########################
@bot.command(name='setInstructor', help='Set member to Instructor.')
@commands.has_role('Instructor')
async def set_instructor(ctx, member:discord.Member):
    ''' set instructor role command '''
    if ctx.channel.name == 'instructor-commands':
        irole = get(ctx.guild.roles, name='Instructor')
        if irole in member.roles:
            await ctx.channel.send(member.name + " is already an Instructor!")
        else:
            await member.add_roles(irole, reason=None, atomic=True)
            await ctx.channel.send(member.name + " has been given Instructor role!")
            channel = get(ctx.guild.text_channels, name='instructor-commands')
            await channel.set_permissions(member, read_messages=True,
            send_messages=True,read_message_history=False)
    else:
        await ctx.channel.send('Not a valid command for this channel')

###########################
# Function: remove_instructor
# Description: Command used to remove a user from Instructor role by instructors
# Inputs:
#      - ctx: context of the command
#      - member: user to remove role
# Outputs:
#      - Sends confirmation back to channel
###########################
@bot.command(name='removeInstructor', help='Remove member from Instructor.')
@commands.has_role('Instructor')
async def remove_instructor(ctx, member:discord.Member):
    ''' remove instructor role command '''
    if ctx.channel.name == 'instructor-commands':
        irole = get(ctx.guild.roles, name='Instructor')
        if irole not in member.roles:
            await ctx.channel.send(member.name + " is not an Instructor!")
        else:
            await member.remove_roles(irole, reason=None, atomic=True)
            await ctx.channel.send(member.name + " has been removed from Instructor role!")
            channel = get(ctx.guild.text_channels, name='instructor-commands')
            await channel.set_permissions(member, overwrite=None)
    else:
        await ctx.channel.send('Not a valid command for this channel')

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
    # make sure to check that this is actually being answered in the Q&A channel
    if ctx.channel.name == 'q-and-a':
        await qna.answer(ctx, q_num, answer)
    else:
        await ctx.author.send('Please send answers to the #q-and-a channel.')
        await ctx.message.delete()
###########################
# Function: ping
# Description: Shows latency for debugging
###########################

@bot.command(name='ping', help='Returns Latency')

async def ping(ctx):
    start=time()
    message=await ctx.send(f"Pong! : {bot.latency*1000:,.0f} ms")
    end=time()
    await message.edit(content="Pong! : "+str(int(bot.latency*1000))+" ms."+
    " Response time : "+str(int((end-start)*1000))+" ms.")
###########################
# Function: stats
# Description: Shows stats like
###########################

@bot.command(name='stats', help='shows bot stats')

async def show_stats(ctx):
    embed = Embed(title="Bot stats",
                    colour=ctx.author.colour,
                    thumbnail=bot.user.avatar_url,
                    timestamp=datetime.utcnow())

    proc = Process()
    with proc.oneshot():
        uptime = timedelta(seconds=time()-proc.create_time())
        cpu_time = timedelta(seconds=(cpu := proc.cpu_times()).system + cpu.user)
        mem_total = virtual_memory().total / (1024**2)
        mem_of_total = proc.memory_percent()
        mem_usage = mem_total * (mem_of_total / 100)

    fields = [
        ("Bot version", BOT_VERSION, True),
        ("Python version", python_version(), True),
        ("discord.py version", discord_version, True),
        ("Uptime", uptime, True),
        ("CPU time", cpu_time, True),
        ("Memory usage", f"{mem_usage:,.3f} / {mem_total:,.0f} MiB ({mem_of_total:.0f}%)", True),
        ("Users", f"{ctx.guild.member_count:,}", True)
    ]

    for name, value, inline in fields:
        embed.add_field(name=name, value=value, inline=inline)

    await ctx.send(embed=embed)
###########################
# Function: poll
# Description: Poll functionality for  administrators
# Inputs:
#      - ctx: context of the command
#      - minutes: minutes in integer
#      - question: Enter the topic on which the poll is created
#      - options: options for poll
# Outputs:
#      - Poll in discord channel. results after the specified time.
###########################
polls=[]
scheduler = AsyncIOScheduler()
@bot.command(name='poll', help='Set Poll for a specified time and topic.')
@commands.has_role('Instructor')

async def create_poll(ctx, hours: int, question: str, *options):

    if len(options) > 10:
        await ctx.send("You can only supply a maximum of 10 options.")

    else:
        embed = Embed(title="Poll ‼",
                        description=question,
                        colour=ctx.author.colour,
                        timestamp=datetime.utcnow())

        fields = [("Options", "\n".join([f"{numbers[idx]} {option}" for idx,
        option in enumerate(options)]), False),
        ("Instructions", "React to cast a vote!", False),
        ("Duration","The Voting will end in "+str(hours)+" Minutes",False)]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        message = await ctx.send(embed=embed)

        for emoji in numbers[:len(options)]:
            await message.add_reaction(emoji)

        polls.append((message.channel.id, message.id))
        scheduler.add_job(complete_poll, "interval",
        minutes=hours,args=(message.channel.id, message.id))
        scheduler.start()

async def complete_poll(channel_id, message_id):
    message = await bot.get_channel(channel_id).fetch_message(message_id)

    most_voted = max(message.reactions, key=lambda r: r.count)

    await message.channel.send("The results are in and option "+most_voted.emoji+
    " was the most popular with "+str(most_voted.count-1)+" votes!")
    polls.remove((message.channel.id, message.id))
    scheduler.shutdown()

@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id in (poll[1] for poll in polls):
        message = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)

        for reaction in message.reactions:
            if (not payload.member.bot
                and payload.member in await reaction.users().flatten()
                and reaction.emoji != payload.emoji.name):
                await message.remove_reaction(reaction.emoji, payload.member)

###########################
# Function: custom-profanity
# Description: Define a word to be added to the profanity filter
# Inputs:
#      - ctx: context of the command
###########################
@bot.command(name = 'custom', help = 'Add word to profanity filter')
async def custom_profanity(ctx, pword):
    ''' adding custom word to profanity list '''
    profanity.custom_words.append(pword)
    await ctx.message.delete()

###########################
# Function: attendance
# Description: Gets the attendance when requested by the instructor for audio channel
# Inputs:
#      - ctx: context of the command
###########################
@bot.command(name='attendance', help='Gets the attendance of voice channel')
@commands.has_role('Instructor')
async def attend(ctx):
    await attendance.compute(bot, ctx)

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

    if ctx.author.id != Test_bot_application_ID:
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
    if ctx.author.id != Test_bot_application_ID:
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
