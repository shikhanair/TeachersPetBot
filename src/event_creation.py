###########################
# Functionality for creating new events
###########################
from os import times
from discord.ext.commands.core import check
from discord_components import Button, ButtonStyle, Select, SelectOption
import datetime
import validators
import office_hours
import cal

import db

BOT = None

###########################
# Function: get_times
# Description: helper function for acquiring the times an instructor wants event to be held during
# Inputs:
#      - ctx: context of this discord message
#      - event_type: type of event which times are being asked for
#      - command_invoker: discord user who is creating event
# Outputs: the begin and end times for the event
###########################
async def get_times(ctx, event_type, command_invoker):
    ''' get times input flow '''
    await ctx.send(
        f'Which times would you like the {event_type} to be on?\n'
        'Enter in format `<begin_time>-<end_time>`, and times should be in 24-hour format.\n'
        f'For example, setting {event_type} from 9:30am to 1pm can be done as 9:30-13'
    )

    msg = await BOT.wait_for('message', check=lambda m: m.author == command_invoker)

    times = msg.content.strip().split('-')
    if len(times) != 2:
        await ctx.send('Incorrect input. Aborting')
        return

    new_times = []
    for t in times:
        parts = t.split(':')
        if len(parts) == 1:
            new_time = (int(parts[0]), 0)
        elif len(parts) == 2:
            new_time = (int(parts[0]), int(parts[1]))
        new_times.append(new_time)
    
    if len(new_times) != 2:
        await ctx.send('Incorrect input. Aborting')
        return
    
    return new_times

###########################
# Function: create_event
# Description: creates an event by the specifications of the instructor creating the event
# Inputs:
#      - ctx: context of this discord message
#      - testing_mode: flag indicating whether this event is being created during a system test
# Outputs: new event created in database
###########################
async def create_event(ctx, testing_mode):
    ''' create event input flow '''
    command_invoker = ctx.author

    if ctx.channel.name == 'instructor-commands':
        await ctx.send(
            'Which type of event would you like to create?',
            components=[
                Button(style=ButtonStyle.blue, label='Assignment', custom_id='assignment'),
                Button(style=ButtonStyle.green, label='Exam', custom_id='exam'),
                Button(style=ButtonStyle.red, label='Office Hour', custom_id='office-hour')
            ],
        )

        button_clicked = (await BOT.wait_for('message')).content if testing_mode else (await BOT.wait_for('button_click')).custom_id
        if button_clicked == 'assignment':
            await ctx.send('What would you like the assignment to be called')
            msg = await BOT.wait_for('message', check=lambda m: m.author == command_invoker)
            title = msg.content.strip()

            await ctx.send('Link associated with submission? Type N/A if none')
            msg = await BOT.wait_for('message', check=lambda m: m.author == command_invoker)
            link = msg.content.strip() if msg.content.strip() != 'N/A' else None

            if link and not validators.url(link):
                await ctx.send('Invalid URL. Aborting.')
                return

            await ctx.send('Extra description for assignment? Type N/A if none')
            msg = await BOT.wait_for('message', check=lambda m: m.author == command_invoker)
            description = msg.content.strip() if msg.content.strip() != 'N/A' else None

            await ctx.send('What is the due date of this assignment?\n' +
                'Enter in format `MM-DD-YYYY`')
            msg = await BOT.wait_for('message', check=lambda m: m.author == command_invoker)
            date = msg.content.strip()

            is_valid = len(date) == 10
            try:
                datetime.datetime.strptime(date, '%m-%d-%Y')
            except ValueError:
                is_valid = False

            if not is_valid:
                await ctx.send('Invalid date. Aborting.')
                return

            await ctx.send('What time is this assignment due?\nEnter in 24-hour format' +
                ' e.g. an assignment due at 11:59pm can be inputted as 23:59')
            msg = await BOT.wait_for('message', check=lambda m: m.author == command_invoker)
            t = msg.content.strip()

            try:
                t = datetime.datetime.strptime(t, '%H:%M')
            except ValueError:
                try:
                    t = datetime.datetime.strptime(t, '%H')
                except ValueError:
                    await ctx.send('Incorrect input. Aborting.')
                    return

            db.mutation_query(
                'INSERT INTO assignments VALUES (?, ?, ?, ?, ?, ?, ?)',
                [ctx.guild.id, title, link, description, date, t.hour, t.minute]
            )

            # TODO add assignment to events list

            await ctx.send('Assignment successfully created!')
            await cal.display_events(None)
        elif interaction.custom_id == 'exam':
            await ctx.send('What is the title of this exam?')
            msg = await BOT.wait_for('message', check=lambda m: m.author == command_invoker)
            title = msg.content.strip()

            await ctx.send('What content is this exam covering?')
            msg = await BOT.wait_for('message', check=lambda m: m.author == command_invoker)
            description = msg.content.strip()

            await ctx.send('What is the date of this exam?\nEnter in format `MM-DD-YYYY`')
            msg = await BOT.wait_for('message', check=lambda m: m.author == command_invoker)
            date = msg.content.strip()

            is_valid = len(date) == 10
            try:
                datetime.datetime.strptime(date, '%m-%d-%Y')
            except ValueError:
                is_valid = False

            if not is_valid:
                await ctx.send('Invalid date. Aborting.')
                return

            times = await get_times(ctx, 'exam', command_invoker)
            if not times:
                return

            ((begin_hour, begin_minute), (end_hour, end_minute)) = times

            db.mutation_query(
                'INSERT INTO exams VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                [ctx.guild.id, title, description, date,
                 begin_hour, begin_minute, end_hour, end_minute]
            )

            # TODO add exam to events list

            await ctx.send('Exam successfully created!')
            await cal.display_events(None)
        elif interaction.custom_id == 'office-hour':
            all_instructors = []
            for mem in ctx.guild.members:
                is_instructor = next((role.name == 'Instructor'
                    for role in mem.roles), None) is not None
                if is_instructor:
                    all_instructors.append(mem)
            
            if len(all_instructors) < 1:
                await ctx.send('There are no instructors in the guild. Aborting')
                return

            options = [SelectOption(label=instr.name, value=instr.name)
                for instr in all_instructors]

            await ctx.send(
                'Which instructor will this office hour be for?',
                components=[
                    Select(
                        placeholder='Select an instructor', #all_instructors[0].name,
                        options=options
                    )
                ]
            )

            # instr_select_interaction = await BOT.wait_for('select_option')
            # instructor = instr_select_interaction.values[0]
            instructor = ((await BOT.wait_for('message')).content
                if testing_mode else (await BOT.wait_for('select_option')).values[0])

            await ctx.send(
                'Which day would you like the office hour to be on?',
                components=[
                    Select(
                        placeholder='Select a day',
                        options=[
                            SelectOption(label='Monday', value='Mon'),
                            SelectOption(label='Tuesday', value='Tue'),
                            SelectOption(label='Wednesday', value='Wed'),
                            SelectOption(label='Thursday', value='Thu'),
                            SelectOption(label='Friday', value='Fri'),
                            SelectOption(label='Saturday', value='Sat'),
                            SelectOption(label='Sunday', value='Sun')
                        ]
                    )
                ]
            )

            # day_interaction = await BOT.wait_for('select_option', check=lambda x: x.values[0] in
            # ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'))
            day = (
                (await BOT.wait_for('message')).content
                if testing_mode else
                (await BOT.wait_for('select_option', check=lambda x: x.values[0] in
                    ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'))).values[0]
            )
            # day = day_interaction.values[0]
            day_num = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun').index(day)

            times = await get_times(ctx, 'office hour', command_invoker)
            if not times:
                return

            ((begin_hour, begin_minute), (end_hour, end_minute)) = times

            office_hours.add_office_hour(
                ctx.guild,
                office_hours.TaOfficeHour(
                    instructor,
                    day_num,
                    (datetime.time(hour=begin_hour, minute=begin_minute),
                     datetime.time(hour=end_hour, minute=end_minute))
                )
            )

            db.mutation_query(
                'INSERT INTO ta_office_hours VALUES (?, ?, ?, ?, ?, ?, ?)',
                [ctx.guild.id, instructor, day_num, begin_hour, begin_minute, end_hour, end_minute]
            )

            await ctx.send('Office hour successfully created!')

    else:
        await ctx.author.send('`!create` can only be used in the `instructor-commands` channel')
        await ctx.message.delete()

###########################
# Function: init
# Description: initializes this module, giving it access to discord bot
# Inputs:
#      - b: discord bot
# Outputs: None
###########################
def init(b):
    ''' initialize event creation '''
    global BOT
    BOT = b
