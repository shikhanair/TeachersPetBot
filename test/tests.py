import os
import discord
from dotenv import load_dotenv

import test_office_hours
import test_event_creation
import test_qna

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
        await test_qna.test(testing_bot, TEST_GUILD_ID)
        await test_office_hours.test(testing_bot, TEST_GUILD_ID)
        await test_event_creation.test(testing_bot, TEST_GUILD_ID)
    except Exception as ex:
        print('exception: ', ex)
        exit_status = 1
    finally:
        await end_tests()

    await testing_bot.close()
    print('exit_status: ', exit_status)
    assert exit_status == 0

async def begin_tests():
    await testing_bot.get_guild(TEST_GUILD_ID).text_channels[0].send('!begin-tests')

async def end_tests():
    # TODO maybe move the logic in here
    await testing_bot.get_guild(TEST_GUILD_ID).text_channels[0].send('!end-tests')

if __name__ == '__main__':
    testing_bot.run(TOKEN)