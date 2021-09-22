from os import times
from discord.ext.commands.core import check
from discord_components import Button, ButtonStyle, Select, SelectOption
import datetime

import db

bot = None

async def get_times(ctx, event_type, command_invoker):
    await ctx.send(
        f'Which times would you like the {event_type} to be on?\n'
        'Enter in format `<begin_time>-<end_time>`, and times should be in 24-hour format.\n'
        f'For example, setting {event_type} from 9:30am to 1pm can be done as 9:30-13'
    )

    msg = await bot.wait_for('message', check=lambda m: m.author == command_invoker)

    times = msg.content.split('-')
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


async def create_event(ctx):
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

        interaction = await bot.wait_for('button_click')
        if interaction.custom_id == 'assignment':
            await ctx.send('What would you like the assignment to be called')
        if interaction.custom_id == 'exam':
            await ctx.send('What is the title of this exam?')
            msg = await bot.wait_for('message', check=lambda m: m.author == command_invoker)
            title = msg.content

            await ctx.send('What content is this exam covering?')
            msg = await bot.wait_for('message', check=lambda m: m.author == command_invoker)
            description = msg.content

            await ctx.send('What is the date of this exam?\nEnter in format `MMDDYYYY`')
            msg = await bot.wait_for('message', check=lambda m: m.author == command_invoker)
            date = msg.content

            is_valid = len(date) == 8
            try:
                datetime.datetime.strptime(date, '%M%D%Y')
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
                [ctx.guild.id, title, description, date, begin_hour, begin_minute, end_hour, end_minute]
            )

            await ctx.send('Exam successfully created!')
        if interaction.custom_id == 'office-hour':
            all_instructors = []
            for mem in ctx.guild.members:
                is_instructor = next((role.name == 'Instructor' for role in mem.roles), None) is not None
                if is_instructor:
                    all_instructors.append(mem)
            
            if len(all_instructors) < 1:
                await ctx.send('There are no instructors in the guild. Aborting')
                return

            options = [SelectOption(label=instr.name, value=instr.name) for instr in all_instructors]
            
            await ctx.send(
                'Which instructor will this office hour be for?',
                components=[
                    Select(
                        placeholder='Select an instructor', #all_instructors[0].name,
                        options=options
                    )
                ]
            )

            instr_select_interaction = await bot.wait_for('select_option')
            instructor = instr_select_interaction.values[0]

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

            day_interaction = await bot.wait_for('select_option', check=lambda x: x.values[0] in ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'))
            day = day_interaction.values[0]
            day_num = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun').index(day)

            times = await get_times(ctx, 'office hour', command_invoker)
            if not times:
                return

            ((begin_hour, begin_minute), (end_hour, end_minute)) = times

            # begin_time = datetime.time(hour=begin_hour, minute=begin_minute)
            # end_time = datetime.time(hour=end_hour, minute=end_minute)

            db.mutation_query(
                'INSERT INTO ta_office_hours VALUES (?, ?, ?, ?, ?, ?, ?)',
                [ctx.guild.id, instructor, day_num, begin_hour, begin_minute, end_hour, end_minute]
            )

            await ctx.send('Office hour successfully created!')

    else:
        await ctx.author.send('`!create` can only be used in the `instructor-commands` channel')
        await ctx.message.delete()

        
def init(b):
    global bot
    bot = b