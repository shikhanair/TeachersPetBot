import db
import discord

from discord_components import Button, ButtonStyle, Select, SelectOption
from datetime import datetime, time, timezone

bot = None
calendar_embed = None
msg = None 

async def display_events(ctx):
    global msg
    
    # recreate the embed from the database
    update_calendar()
    
    # if it was never created, send the first message
    if not msg:
        msg = await ctx.send(embed=calendar_embed)
    else:
        # otherwise, edit the saved message from earlier
        await msg.edit(embed=calendar_embed)

def update_calendar():
    global calendar_embed
    
    # create an Embed with a title and description of color 'currently BLUE'
    calendar_embed = discord.Embed(title="The Course Calendar, sire", description="All of the class assignments and exams!", color=0x0000FF)
    
    # make a list that contains the string representing the event that has the comparison item as the first index
    # which is the date, we are comparing as strings but still works for ordering events by date
    # do this for the events we care about in the calendar 'assignments and exams'
    assignments = []
    for title, link, desc, date, due_hr, due_min in db.select_query('SELECT ' +
                                                                        'title, link, desc, date, due_hr, due_min ' +
                                                                    'FROM ' +
                                                                        'assignments ' +
                                                                    'ORDER BY ' +
                                                                        'date ASC, ' +
                                                                        'due_hr ASC, ' +
                                                                        'due_min ASC'):
        assignments.append([ f'{date} {due_hr}:{due_min}', f'{date} {due_hr}:{due_min}\n{title}\n{desc}\n{link}\n\n'])
    
    exams = []
    for title, desc, date, begin_hr, begin_min, end_hr, end_min in db.select_query('SELECT ' +
                                                                        'title, desc, date, begin_hr, begin_min, end_hr, end_min ' +
                                                                    'FROM ' +
                                                                        'exams ' +
                                                                    'ORDER BY ' +
                                                                        'date ASC, ' +
                                                                        'begin_hr ASC, '
                                                                        'begin_min ASC'):
        exams.append([ f'{date} {begin_hr}:{begin_min}', f'{date} {begin_hr}:{begin_min} - {end_hr}:{end_min}\n{title}\n{desc}\n\n'])

    # get current time for comparison and make sure it is of same string format
    current_time = datetime.now().strftime('%m-%d-%Y %H:%M')
    #Time in EST: 2017-01-19 08:06:14
    
    i = 0
    j = 0
    
    # 2 lists for fields in the calendar
    past_events = ''
    #current_events = ''
    future_events = ''
    
    # go through the sorted lists and take the earliest date, moving the index of each until all lists are placed
    # into one of the defined areas
    while (i != len(exams) or j != len(assignments)):
        if (i == len(exams) or (j != len(assignments) and assignments[j][0] < exams[i][0])):
            if (assignments[j][0] < current_time):
                past_events += assignments[j][1]
            else:
                future_events += assignments[j][1]
            j += 1
        else:
            if (exams[i][0] < current_time):
                past_events += exams[i][1]
            else:
                future_events += exams[i][1]
            i += 1
    
    # add the built strings to the embed
    if past_events != '':
        calendar_embed.add_field(name="Past Events", value=past_events, inline=True)
    
    #calendar_embed.add_field(name="Current Events", value=events, inline=False)
    
    if future_events != '':
        calendar_embed.add_field(name="Coming up", value=future_events, inline=True)
    
    # mark the time that this was done for both creation and editing
    # NOTE - we put in EST because we are EST
    timeNow = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' EST'
    calendar_embed.set_footer(text=f"{timeNow}")

async def init(b):
    global bot
    
    bot = b
    for guild in bot.guilds:
        flag = False
        for channel in guild.text_channels:
            if(channel.name == 'course-calendar'):
                flag = True
        
        if(flag == False):
            channel = await guild.create_text_channel('course-calendar')
            await display_events(channel)