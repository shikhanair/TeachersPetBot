import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TESTING_BOT_TOKEN')

testing_bot = discord.Client()

TEST_GUILD_ID = 0

@testing_bot.event
async def on_ready():
    print('Testing bot running')
    print('------')
    await test_oh_queue_individ()

async def get_queue():
    bot_queue_resp = await testing_bot.wait_for('message', check=lambda m: 'Queue' in m.content)
    return bot_queue_resp.split('\n')[2:]

async def test_oh_queue_individ():
    oh_channel = next((testing_bot.get_guild(TEST_GUILD_ID).text_channels), None)
    if not oh_channel:
        assert False
    await oh_channel.send('!oh enter')

    queue = await get_queue()
    assert len(queue) == 1 and 'TestingBot' in queue[0]

    await oh_channel.send('!oh exit')

    queue = await get_queue()
    assert queue[0] == '(The queue is currently empty)'


testing_bot.run(TOKEN)