
"""Attendance functionality"""
import os
import discord
from discord import Embed
from dotenv import load_dotenv

load_dotenv()
main_bot = os.getenv('DICORD_BOT_NAME')
test_bot = os.getenv('TEST_BOT_NAME')

###########################
# Function: compute
# Description: Finds attendees and absentees of class
# Inputs:
#      - bot: bot that sends commands to test TeachersPetBot
#      - ctx: Context of the function activation
# Outputs: None
###########################
async def compute(bot, ctx):
    """Only function that computes attendance"""
    if ctx.channel.name == 'instructor-commands':
        attendees = []
        absentees = []
        wanted_channel_id = 0

        for channel in ctx.guild.channels:
            if channel.name == "General":
                wanted_channel_id = channel.id

        audio_channel = bot.get_channel(wanted_channel_id)
        text_channel = bot.get_channel(ctx.channel.id)

        embed = Embed(title="Attendance Sheet",
                      colour=discord.Colour.blue())

        for attendee in audio_channel.members:
            attendees.append(attendee.name)
        if attendees:
            embed.add_field(name=f"Attendees: {len(attendees)}",
                            value='\n'.join(attendees), inline=True)
        else:
            embed.add_field(name="Attendees: 0", value="None", inline=True)

        for student in text_channel.members:
            if student.name not in attendees and \
                    student.name != main_bot and \
                    student.name != test_bot:
                absentees.append(student.name)
        if absentees:
            embed.add_field(name=f"Absentees: {len(absentees)}",
                            value='\n'.join(absentees), inline=True)
        else:
            embed.add_field(name="Absentees: 0",
                            value="None", inline=True)
        await ctx.send(embed=embed)

    else:
        await ctx.message.delete()
        await ctx.send('Command runs only in the instructor-commands channel')
