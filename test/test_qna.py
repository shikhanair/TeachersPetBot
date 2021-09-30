###########################
# Tests Q-and-A functionality
###########################
import discord
from time import sleep


###########################
# Function: test
# Description: runs each test
# Inputs:
#      - testing_bot: bot that sends commands to test TeachersPetBot
#      - guild_id: id of the guild that is using the TeachersPetBot
# Outputs: None
###########################
async def test(testing_bot, guild_id):
    await test_question(testing_bot)
    await test_answer(testing_bot, guild_id)
    await test_instr_answer(testing_bot, guild_id)


###########################
# Function: test_question
# Description: tests questioning functionality
# Inputs:
#      - testing_bot: bot that sends commands to test TeachersPetBot
# Outputs: None
###########################
async def test_question(testing_bot):
    print('testing question')
    qna_channel = discord.utils.get(testing_bot.get_all_channels(), name='q-and-a')
    await qna_channel.send('!ask \"Hello\"')

    sleep(0.5)

    messages = await qna_channel.history(limit=1).flatten()
    for m in messages:
        assert 'Q1: Hello' in m.content


###########################
# Function: test_answer
# Description: tests answering functionality as a student
# Inputs:
#      - testing_bot: bot that sends commands to test TeachersPetBot
#      - guild_id: id of the guild that is using the TeachersPetBot
# Outputs: None
###########################
async def test_answer(testing_bot, guild_id):
    print('testing answer')

    # make sure bot is not an instructor
    guild = testing_bot.get_guild(guild_id)
    role = discord.utils.get(guild.roles, name="Instructor")
    member = guild.get_member(testing_bot.user.id)
    if "instructor" in [y.name.lower() for y in member.roles]:
        await member.remove_roles(role)

    qna_channel = discord.utils.get(testing_bot.get_all_channels(), name='q-and-a')
    await qna_channel.send('!answer 1 \"World\"')

    sleep(1.5)

    messages = await qna_channel.history(limit=1).flatten()
    for m in messages:
        assert 'Student Ans: World' in m.content

###########################
# Function: test_instr_answer
# Description: tests answering functionality as an instructor
# Inputs:
#      - testing_bot: bot that sends commands to test TeachersPetBot
#      - guild_id: id of the guild that is using the TeachersPetBot
# Outputs: None
###########################
async def test_instr_answer(testing_bot, guild_id):
    print('testing instructor answer')

    # Add instructor role to bot
    guild = testing_bot.get_guild(guild_id)
    role = discord.utils.get(guild.roles, name="Instructor")
    member = guild.get_member(testing_bot.user.id)
    await member.add_roles(role)

    # answer question as instructor
    qna_channel = discord.utils.get(testing_bot.get_all_channels(), name='q-and-a')
    await qna_channel.send('!answer 1 \"Hello World\"')

    sleep(1.5)

    # check message was updated
    messages = await qna_channel.history(limit=1).flatten()
    for m in messages:
        assert 'Instructor Ans: Hello World' in m.content

    # remove instructor role from bot
    await member.remove_roles(role)

