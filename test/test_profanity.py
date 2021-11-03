###########################
# Tests Profanity
###########################
from time import sleep
import discord
###########################
# Function: test
# Description: runs each test
# Inputs:
#      - testing_bot: bot that sends commands to test TeachersPetBot
#      - guild_id: id of the guild that is using the TeachersPetBot
# Outputs: None
###########################
async def test(testing_bot, guild_id):
    await test_profanity_1(testing_bot)
    await test_profanity_2(testing_bot)
    await test_profanity_3(testing_bot)

    await test_custom_profanity_1(testing_bot)
    await test_custom_profanity_2(testing_bot)
    await test_custom_profanity_3(testing_bot)

###########################
# Function: test_profanity
# Description: tests profanity filter
# Inputs:
#      - testing_bot: bot that sends commands to test TeachersPetBot
# Outputs: None
###########################
async def test_profanity_1(testing_bot):
    print('testing profanity - 1')
    qna_channel = discord.utils.get(testing_bot.get_all_channels(), name='q-and-a')
    await qna_channel.send('shit')
    sleep(5.0)
    messages = await qna_channel.history(limit=1).flatten()

    for m in messages:
        assert '****' in m.content

async def test_profanity_2(testing_bot):
    print('testing profanity - 2')
    qna_channel = discord.utils.get(testing_bot.get_all_channels(), name='q-and-a')
    await qna_channel.send('fuck')
    sleep(5.0)
    messages = await qna_channel.history(limit=1).flatten()

    for m in messages:
        assert '****' in m.content

async def test_profanity_3(testing_bot):
    print('testing profanity - 3')
    qna_channel = discord.utils.get(testing_bot.get_all_channels(), name='q-and-a')
    await qna_channel.send('shit')
    sleep(5.0)
    messages = await qna_channel.history(limit=1).flatten()

    for m in messages:
        assert '****' in m.content

###########################
# Function: test_profanity
# Description: tests profanity filter
# Inputs:
#      - testing_bot: bot that sends commands to test TeachersPetBot
# Outputs: None
###########################
async def test_custom_profanity_1(testing_bot):
    print('testing custom profanity - 1')
    qna_channel = discord.utils.get(testing_bot.get_all_channels(), name='q-and-a')
    await qna_channel.send('!custom "word"')
    sleep(2.0)
    await qna_channel.send('word')
    sleep(5.0)
    messages = await qna_channel.history(limit=1).flatten()

    for m in messages:
        assert '****' in m.content

async def test_custom_profanity_2(testing_bot):
    print('testing custom profanity - 2')
    qna_channel = discord.utils.get(testing_bot.get_all_channels(), name='q-and-a')
    await qna_channel.send('!custom "fine"')
    sleep(2.0)
    await qna_channel.send('fine')
    sleep(5.0)
    messages = await qna_channel.history(limit=1).flatten()

    for m in messages:
        assert '****' in m.content

async def test_custom_profanity_3(testing_bot):
    print('testing custom profanity - 3')
    qna_channel = discord.utils.get(testing_bot.get_all_channels(), name='q-and-a')
    await qna_channel.send('!custom "man"')
    sleep(2.0)
    await qna_channel.send('man')
    sleep(5.0)
    messages = await qna_channel.history(limit=1).flatten()

    for m in messages:
        assert '****' in m.content
