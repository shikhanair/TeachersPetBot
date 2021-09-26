import db
import discord
from discord_components import Button, ButtonStyle, Select, SelectOption

async def display_events(ctx):
    embed=discord.Embed(title="Event List", description="All of the class events.", color=0x0000FF, author=ctx.author)
    
    office_hours = ''
    for ta, day, begin_hr, begin_min, end_hr, end_min in db.select_query('SELECT ta, day, begin_hr, begin_min, end_hr, end_min FROM ta_office_hours'):
        office_hours += f'{ta} {day} {begin_hr} {begin_min} {end_hr} {end_min}\n'

    assignments = ''
    for title, link, desc, date, due_hr, due_min in db.select_query('SELECT title, link, desc, date, due_hr, due_min FROM assignments'):
        assignments += f'{title} {link} {desc} {date} {due_hr} {due_min}\n'
    
    exams = ''
    for title, desc, date, begin_hr, begin_min, end_hr, end_min in db.select_query('SELECT title, desc, date, begin_hr, begin_min, end_hr, end_min FROM exams'):
        exams += f'{title} {desc} {date} {begin_hr} {begin_min} {end_hr} {end_min}\n'
        
    embed.add_field(name="Office Hours🎣", value=office_hours, inline=False) 
    embed.add_field(name="Assignments", value=assignments, inline=False)
    embed.add_field(name="Exams", value=exams, inline=False)

    embed.set_footer(text="Additional Info: Nothing")
    
    await ctx.send(embed=embed)



def init(b):
    global bot
    
    bot = b