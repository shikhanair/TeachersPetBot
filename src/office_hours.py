###########################
# Functionality related to administering office hours
###########################
from datetime import datetime, time
import discord
from discord.ext import tasks
from discord.utils import get

import db


###########################
# Class: Group
# Description: contains information about an office hour group
###########################
class Group:
    def __init__(self, student, group_id):
        self.group_members = [student]
        self.group_id = group_id

###########################
# Class: OfficeHourQueue
# Description: contains information about an office hour queue
###########################
class OfficeHourQueue:
    def __init__(self, ta_name, text_channel, voice_channel, waiting_room):
        self.current_student = None
        self.queue = []
        self.prev_queue_message = None
        self.ta_name = ta_name
        self.text_channel = text_channel
        self.voice_channel = voice_channel
        self.waiting_room = waiting_room
        self.next_grp_id = 0

    ###########################
    # Method: enqueue
    # Description: adds a student to the office hour queue
    # Inputs:
    #      - student: student to add to the office hour queue
    # Outputs: None
    ###########################
    def enqueue(self, student):
        self.queue.append(Group(student, f'{self.next_grp_id:03d}'))
        self.next_grp_id = (self.next_grp_id + 1) % 1000

    ###########################
    # Method: display_queue
    # Description: displays the office hour queue in the office hour channel
    # Outputs: office hour queue as a message in the office hour channel
    ###########################
    async def display_queue(self):
        if self.prev_queue_message:
            await self.prev_queue_message.delete()

        lines = []
        for i, grp in enumerate(self.queue):
            grp_members_str = ', '.join(mem.name for mem in grp.group_members)
            line = f"{i + 1}: {grp_members_str} (group ID: {grp.group_id})"
            lines.append(line)

        queue_str = (
            'Office Hour Queue:\n'
            '------------------\n' +
            ('\n'.join(lines) if len(lines) != 0 else '(The queue is currently empty)')
        )
        self.prev_queue_message = await self.text_channel.send(queue_str)

###########################
# Function: office_hour_command
# Description: handles a command given in an office hour channel
# Inputs:
#      - ctx: context of this discord message
#      - command: office hour command given
#      - args: extra arguments given to command
###########################
async def office_hour_command(ctx, command, *args):
    if ctx.channel.name[:len('office-hour-')] == 'office-hour-':
        ta = ctx.channel.name[len('office-hour-'):]

        office_hour_queue = office_hour_queues[ta]
        queue = office_hour_queue.queue

        is_instructor = 'Instructor' in (r.name for r in ctx.author.roles)

        if command == 'enter' and not is_instructor:
            all_queued_students = []
            for grp in queue:
                all_queued_students.append(*grp.group_members)
            if ctx.author.name not in all_queued_students:
                if len(args) == 0:
                    office_hour_queue.enqueue(ctx.author)
                    await office_hour_queue.display_queue()
                elif len(args) == 1:
                    group_id_to_join = args[0]
                    group_to_join = next((group for group in queue if
                        group_id_to_join == group.group_id), None)
                    if group_to_join:
                        group_to_join.group_members.append(ctx.author)
                        await office_hour_queue.display_queue()
                    else:
                        await ctx.author.send(
                            'The office hour group you have attempted to join does not exist. '
                            'Please ensure you enter a valid group ID when attempting to '
                            'join an office hour group.'
                        )
                await office_hour_queue.waiting_room.set_permissions(
                    ctx.author, read_messages=True, send_messages=True)
            else:
                await ctx.author.send(
                    'You are already in the office hour queue so you cannot join again. '
                    'If you would like to join an office hour group, please exit the queue '
                    'and join the group.'
                )
        elif command == 'exit' and not is_instructor:
            queued_group = next(
                (group for group in queue if ctx.author in group.group_members),
                None
            )
            if queued_group:
                queued_group.group_members.remove(ctx.author)
                if len(queued_group.group_members) == 0:
                    queue.remove(queued_group)
                await office_hour_queue.waiting_room.set_permissions(ctx.author, overwrite=None)
                await office_hour_queue.display_queue()
        elif command == 'next' and is_instructor:
            voice_channel = office_hour_queue.voice_channel
            waiting_room = office_hour_queue.waiting_room

            if office_hour_queue.current_student:
                await voice_channel.set_permissions(
                    office_hour_queue.current_student,
                    overwrite=None
                )

            next_group = queue.pop(0)
            for member in next_group.group_members:
                await voice_channel.set_permissions(member, read_messages=True, send_messages=True)
                await waiting_room.set_permissions(member, overwrite=None)

                message = (
                    f'{office_hour_queue.ta_name} is ready to help '
                    f"{'you' if len(next_group.group_members) == 1 else 'your group'}."
                    'Please join the office hour voice channel.'
                )
                await member.send(message)
            await office_hour_queue.display_queue()
    else:
        await ctx.author.send('The `!oh` command is only valid in office hour text channels.')

    await ctx.message.delete()

###########################
# Function: open_oh
# Description: opens an office hour for students to get help from
# Inputs:
#      - guild: discord guild this office hour is relevant for
#      - ta: name of TA who is holding this office hour
# Outputs: creation of channels relevant to office hour
###########################
async def open_oh(guild, ta):
    category = await guild.create_category_channel(f'Office Hour {ta}')

    instructor_role = get(guild.roles, name='Instructor')
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False),
        instructor_role: discord.PermissionOverwrite(read_messages=True, send_messages=True)
    }

    ta_name_channelified = ta.lower().replace(" ", "-")
    text_channel = await category.create_text_channel(f'office-hour-{ta_name_channelified}')
    voice_channel = await category.create_voice_channel(
        f'office-hour-{ta_name_channelified}', overwrites=overwrites)
    waiting_room = await category.create_voice_channel(
        f'office-hour-{ta_name_channelified}-waiting-list', overwrites=overwrites)

    await text_channel.send(
        f"Welcome to {ta}'s office hour!\n"
        'To join the queue, please type `!oh enter` in this channel. '
        'If you would like to join an existing office hour group, type `!oh enter <groupID>\n`'
        'If you would like to exit the queue, please type `!oh exit`.\n'
        f'You may join the waiting list channel (office-hour-{ta_name_channelified}-waiting-list)'
        "while you wait for your turn if you'd like. When it is your turn, you will be notified."
    )

    office_hour_queues[ta_name_channelified] = OfficeHourQueue(ta, text_channel, voice_channel,
        waiting_room)

###########################
# Function: close_oh
# Description: closes an office hour session
# Inputs:
#      - guild: discord guild this office hour is relevant for
#      - ta: name of TA who is holding this office hour
# Outputs: deletion of channels relevant to office hour
###########################
async def close_oh(guild, ta):
    ta_name_channelified = ta.lower().replace(" ", "-")
    channels_to_delete = [
        next((chan for chan in guild.text_channels if chan.name ==
            f'office-hour-{ta_name_channelified}'), None),
        next((chan for chan in guild.voice_channels if chan.name ==
            f'office-hour-{ta_name_channelified}'), None),
        next((chan for chan in guild.voice_channels if chan.name ==
            f'office-hour-{ta_name_channelified}-waiting-list'), None),
        next((cat for cat in guild.categories if cat.name == f'Office Hour {ta}'), None)
    ]

    for channel in channels_to_delete:
        if channel:
            await channel.delete()

    office_hour_queues.pop(ta_name_channelified)

###########################
# Class: TaOfficeHour
# Description: contains information about when an office hour is held
###########################
class TaOfficeHour:
    def __init__(self, ta, day, times):
        self.ta = ta
        self.day = day
        self.times = times

###########################
# Function: check_office_hour_loop
# Description: runs intermittently to open or close office hours based on the current time
###########################
@tasks.loop(seconds=5)
async def check_office_hour_loop():
    days = ['Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun']
    curr_datetime = datetime.now()
    curr_day = days[curr_datetime.weekday()]
    curr_time = curr_datetime.time()
    for guild in bot.guilds:
        if guild.id in all_guilds_ta_office_hours:
            ta_office_hours = all_guilds_ta_office_hours[guild.id]
            for office_hour in ta_office_hours:
                day = office_hour.day
                if curr_day == day:
                    begin_time, end_time = office_hour.times
                    begin_time = datetime.strptime(str(begin_time).rsplit(' ', 1)[1], '%H:%M:%S').time()
                    end_time = datetime.strptime(str(end_time).rsplit(' ', 1)[1], '%H:%M:%S').time()
                    ta_name_channelified = office_hour.ta.lower().replace(" ", "-")
                    if begin_time <= curr_time <= end_time and ta_name_channelified not in office_hour_queues:
                        print('channel created')
                        await open_oh(guild, office_hour.ta)
                    elif curr_time > end_time and ta_name_channelified in office_hour_queues:
                        print('channel closed')
                        await close_oh(guild, office_hour.ta)

###########################
# Function: add_office_hour
# Description: adds a new TA office hour to the guild
# Inputs:
#      - guild: discord guild this office hour is relevant for
#      - ta_office_hour: TA office hour information
# Outputs: adds a new TA office hour to the system
###########################
def add_office_hour(guild, ta_office_hour):
    all_guilds_ta_office_hours[guild.id].append(ta_office_hour)

bot = None
all_guilds_ta_office_hours = None
office_hour_queues = None
###########################
# Function: init
# Description: initializes office hours module
# Inputs:
#      - b: discord bot
###########################
def init(b):
    global bot
    global all_guilds_ta_office_hours
    global office_hour_queues

    office_hour_queues = {}
    all_guilds_ta_office_hours = {}
    bot = b
    for guild in bot.guilds:
        ta_office_hours = [
            TaOfficeHour(ta, day, (begin_time, end_time))
            for ta, day, begin_time, end_time in db.select_query(
                'SELECT ta, day, begin_time, end_time '
                'FROM ta_office_hours WHERE guild_id = ?', [guild.id])
        ]

        all_guilds_ta_office_hours[guild.id] = ta_office_hours

    check_office_hour_loop.start()
