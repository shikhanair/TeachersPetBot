import os
from time import sleep
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TESTING_BOT_TOKEN')

testing_bot = discord.Client()

TEST_GUILD_ID = 884852950634209300

@testing_bot.event
async def on_ready():
    print('Testing bot running')
    print('------')
    exit_status = 0
    await begin_tests()
    try:
        await test_oh_queue_individ()
    except:
        exit_status = 1
    finally:
        await end_tests()

    quit(exit_status)

async def begin_tests():
    await testing_bot.get_guild(TEST_GUILD_ID).text_channels[0].send('!begin-tests')
    sleep(1)

async def end_tests():
    # TODO maybe move the logic in here
    await testing_bot.get_guild(TEST_GUILD_ID).text_channels[0].send('!end-tests')
    sleep(1)


async def get_queue():
    bot_queue_resp = await testing_bot.wait_for('message', check=lambda m: 'Queue' in m.content)
    return bot_queue_resp.content.split('\n')[2:]

async def test_oh_queue_individ():
    await testing_bot.wait_for('guild_channel_create')
    oh_channel = next((ch for ch in testing_bot.get_guild(TEST_GUILD_ID).text_channels if 'office-hour-test' in ch.name), None)
    if not oh_channel:
        assert False
    await oh_channel.send('!oh enter')

    queue = await get_queue()
    assert len(queue) == 1 and 'TeachersPetBotTester' in queue[0]

    await oh_channel.send('!oh exit')

    queue = await get_queue()
    assert queue[0] == '(The queue is currently empty)'

# def test_oh():
#     testing_bot.run(TOKEN)

testing_bot.run(TOKEN)