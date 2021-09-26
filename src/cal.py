import db
import discord
from discord_components import Button, ButtonStyle, Select, SelectOption
from datetime import datetime, time
from discord.ext import tasks

bot = None
calendar_embed = None

@tasks.loop(seconds=5)
async def display(msg):
    timeNow = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    calendar_embed.set_footer(text=f"Updated: {timeNow}")
    await msg.edit(embed=calendar_embed)


async def display_events(ctx):
    update_calendar()
    
    msg = await ctx.send(embed=calendar_embed)
    
    display.start(msg)

def update_calendar():
    global calendar_embed
    
    calendar_embed = discord.Embed(title="Event List", description="All of the class events.", color=0x0000FF)
    
    '''
    assignments = ''
    for title, link, desc, date, due_hr, due_min in db.select_query('SELECT title, link, desc, date, due_hr, due_min FROM assignments'):
        assignments += f'{title} {link} {desc} {date} {due_hr} {due_min}\n'
    
    exams = ''
    for title, desc, date, begin_hr, begin_min, end_hr, end_min in db.select_query('SELECT title, desc, date, begin_hr, begin_min, end_hr, end_min FROM exams'):
        exams += f'{title} {desc} {date} {begin_hr} {begin_min} {end_hr} {end_min}\n'
    '''
    
    assignments = []
    for title, link, desc, date, due_hr, due_min in db.select_query('SELECT ' +
                                                                        'a.title, a.link, a.desc, a.date, a.due_hr, a.due_min ' +
                                                                    'FROM ' +
                                                                        'assignments AS a ' +
                                                                    'ORDER BY ' +
                                                                        'a.date ASC, ' +
                                                                        'a.due_hr ASC, ' +
                                                                        'a.due_min ASC'):
        assignments.append([ f'{date} {due_hr}:{due_min}', f'{date} {due_hr}:{due_min} - {title}\n\t{desc}\n\t{link}\n'])
    
    exams = []
    for title, desc, date, begin_hr, begin_min, end_hr, end_min in db.select_query('SELECT ' +
                                                                        'e.title, e.desc, e.date, e.begin_hr, e.begin_min, e.end_hr, e.end_min ' +
                                                                    'FROM ' +
                                                                        'exams AS e ' +
                                                                    'ORDER BY ' +
                                                                        'e.date ASC, ' +
                                                                        'e.begin_hr ASC, '
                                                                        'e.begin_min ASC'):
        exams.append([ f'{date} {begin_hr}:{begin_min}', f'{date} {begin_hr}:{begin_min} - {end_hr}:{end_min}\n\t{title}\n\t{desc}\n'])
    
    i = 0
    j = 0
    
    events = ''
    while (i != len(exams) or j != len(assignments)):
        if (i == len(exams) or (j != len(assignments) and assignments[j] < exams[i]) ):
            events += assignments[j][1]
            j += 1
        else:
            events += exams[i][1]
            i += 1
    
    
    calendar_embed.add_field(name="Events", value=events, inline=False)
    
    timeNow = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    calendar_embed.set_footer(text=f"Created: {timeNow}")

def init(b):
    global bot
    
    bot = b