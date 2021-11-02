###########################
# Functionality for creating new events
###########################
import datetime
from discord_components import Button, ButtonStyle, Select, SelectOption
import validators
from discord.utils import get
from utils import wait_for_msg

import office_hours
import cal
import db

BOT = None

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

    if ctx.channel.name == 'instructor-commands':
        await ctx.send(
            'Which type of event would you like to create?',
            components=[
                Button(style=ButtonStyle.blue, label='Assignment', custom_id='assignment'),
                Button(style=ButtonStyle.green, label='Exam', custom_id='exam'),
                Button(style=ButtonStyle.red, label='Office Hour', custom_id='office-hour')
            ],
        )
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        if testing_mode:
            button_clicked = await BOT.wait_for('message', timeout = 5, check = check)
            button_clicked = button_clicked.content
        else:
            button_clicked = (await BOT.wait_for('button_click')).custom_id

        if button_clicked == 'assignment':
            await ctx.send('What would you like the assignment to be called')
            msg = await BOT.wait_for('message', timeout = 60.0, check = check)
            title = msg.content.strip()

            await ctx.send('What is the due date of this assignment?\nEnter in format `MM-DD-YYYY`')
            msg = await BOT.wait_for('message', timeout = 60.0, check = check)
            date = msg.content.strip()
            try:
                datetime.datetime.strptime(date, '%m-%d-%Y')
            except ValueError:
                await ctx.send('Invalid date foamt. Aborting.')
                return

            await ctx.send('What time is this assignment due?\nEnter in 24-hour format' +
                ' e.g. an assignment due at 11:59pm can be inputted as 23:59')
            msg = await BOT.wait_for('message', timeout = 60.0, check = check)
            t = msg.content.strip()
            try:
                datetime.datetime.strptime(t, '%H:%M')
            except ValueError:
                await ctx.send('Invalid Time format. Aborting.')
                return
            deadline = datetime.datetime.strptime(date+' '+t, '%m-%d-%Y %H:%M')

            await ctx.send('Link associated with submission? Type N/A if none')
            msg = await BOT.wait_for('message', timeout = 60.0, check = check)
            link = msg.content.strip() if msg.content.strip() != 'N/A' else None
            if link and not validators.url(link):
                await ctx.send('Invalid URL. Aborting.')
                return

            await ctx.send('Extra description for assignment? Type N/A if none')
            msg = await BOT.wait_for('message', timeout = 60.0, check = check)
            description = msg.content.strip() if msg.content.strip() != 'N/A' else None

            db.mutation_query(
                'INSERT INTO assignments VALUES (?, ?, ?, ?, ?)',
                [ctx.guild.id, title, link, description, deadline]
            )

            # TODO add assignment to events list
            await ctx.send('Assignment successfully created!')
            await cal.display_events(None)
        elif button_clicked == 'exam':
            await ctx.send('What is the title of this exam?')
            msg = await BOT.wait_for('message', timeout = 60.0, check = check)
            title = msg.content.strip()

            await ctx.send('What is the start date of this exam?\nEnter in format `MM-DD-YYYY`')
            msg = await BOT.wait_for('message', timeout = 60.0, check = check)
            date_start = msg.content.strip()
            try:
                datetime.datetime.strptime(date_start, '%m-%d-%Y')
            except ValueError:
                await ctx.send('Invalid date. Aborting.')
                return

            await ctx.send('What is the start time for the exam?\nEnter in 24-hour format' +
                ' e.g. an exam starting at 1:59pm can be inputted as 13:59')
            msg = await BOT.wait_for('message', timeout = 60.0, check = check)
            t_start = msg.content.strip()
            try:
                datetime.datetime.strptime(t_start, '%H:%M')
            except ValueError:
                await ctx.send('Invalid Time format. Aborting.')
                return

            start = datetime.datetime.strptime(date_start+' '+t_start, '%m-%d-%Y %H:%M')

            await ctx.send('What is the end date of this exam?\nEnter in format `MM-DD-YYYY`')
            msg = await BOT.wait_for('message', timeout = 60.0, check = check)
            date_end = msg.content.strip()
            try:
                datetime.datetime.strptime(date_end, '%m-%d-%Y')
            except ValueError:
                await ctx.send('Invalid date. Aborting.')
                return

            await ctx.send('What is the end time for the exam?\nEnter in 24-hour format' +
                ' e.g. an exam ending at 1:59pm can be inputted as 13:59')
            msg = await BOT.wait_for('message', timeout = 60.0, check = check)
            t_end= msg.content.strip()
            try:
                datetime.datetime.strptime(t_end, '%H:%M')
            except ValueError:
                await ctx.send('Invalid Time format. Aborting.')
                return
            end = datetime.datetime.strptime(date_end+' '+t_end, '%m-%d-%Y %H:%M')

            await ctx.send('What is the duration of the exam?\nEnter in minutes' +
                ' e.g. for 1hr 25 mins input as 85 minutes')
            msg = await BOT.wait_for('message', timeout = 60.0, check = check)
            duration = msg.content.strip()

            await ctx.send('description of the exam(like syllabus, online/inperson)? Type N/A if none')
            msg = await BOT.wait_for('message', timeout = 300.0, check = check)
            description = msg.content.strip() if msg.content.strip() != 'N/A' else None

            db.mutation_query(
                'INSERT INTO exams VALUES (?, ?, ?, ?, ?, ?)',
                [ctx.guild.id, title, description, duration, start, end]
            )

            # TODO add exam to events list

            await ctx.send('Exam successfully created!')
            await cal.display_events(None)
        elif button_clicked == 'office-hour':
            leadrole = get(ctx.guild.roles, name='Instructor')
            all_instructors = leadrole.members

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
            if testing_mode:
                instructor = await BOT.wait_for('message', timeout = 5, check = check)
                instructor = instructor.content
            else:
                instructor = (await BOT.wait_for('select_option')).values[0]
            #instructor = ((await BOT.wait_for(ctx.channel)).content if testing_mode else (await BOT.wait_for('select_option')).values[0])

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

            if testing_mode:
                day = await BOT.wait_for('message', timeout = 5, check = check)
                day = day.content
            else:
                day = (await BOT.wait_for('select_option')).values[0]
           
            await ctx.send('What is the start time of the office hour?\nEnter in 24-hour format' +
                ' e.g. an starting at 1:59pm can be inputted as 13:59')
            msg = await BOT.wait_for('message', timeout = 60.0, check = check)
            t_start = msg.content.strip()
            try:
                t_start = datetime.datetime.strptime(t_start, '%H:%M')
            except ValueError:
                await ctx.send('Invalid Time format. Aborting.')
                return

            await ctx.send('What is the end time of the office hour?\nEnter in 24-hour format' +
                ' e.g. an exam ending at 1:59pm can be inputted as 13:59')
            msg = await BOT.wait_for('message', timeout = 60.0, check = check)
            t_end= msg.content.strip()
            try:
                t_end = datetime.datetime.strptime(t_end, '%H:%M')
            except ValueError:
                await ctx.send('Invalid Time format. Aborting.')
                return

            office_hours.add_office_hour(
                ctx.guild,
                office_hours.TaOfficeHour(
                    instructor,
                    day,
                    (t_start, t_end)
                )
            )

            db.mutation_query(
                'INSERT INTO ta_office_hours VALUES (?, ?, ?, ?, ?)',
                [ctx.guild.id, instructor, day, t_start, t_end]
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
