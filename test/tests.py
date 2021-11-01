import os
import discord
from dotenv import load_dotenv

import test_office_hours
import test_event_creation
import test_qna
import test_calendar

load_dotenv()
TOKEN = os.getenv('TESTING_BOT_TOKEN')

testing_bot = discord.Client()

TEST_GUILD_ID = 900108417404923924

async def run_tests():
    exit_status = 0
    await begin_tests()
    try:
        print('testing QNA\n----------')
        await test_qna.test(testing_bot, TEST_GUILD_ID)
        print('testing office hours\n----------')
        await test_office_hours.test(testing_bot, TEST_GUILD_ID)
        print('testing event creation\n----------')
        await test_event_creation.test(testing_bot, TEST_GUILD_ID)
        print('testing calendar\n----------')
        await test_calendar.test(testing_bot, TEST_GUILD_ID)
    except Exception as ex:
        print('exception: ', type(ex).__name__ + ':', ex)
        print('--')
        exit_status = 1
    finally:
        await end_tests()

    await testing_bot.close()
    print('exit_status: ', exit_status)
    assert exit_status == 0


@testing_bot.event
async def on_ready():
    print('Testing bot running')
    print('------')
    await run_tests()

async def begin_tests():
    await next(ch for ch in testing_bot.get_guild(TEST_GUILD_ID).text_channels if ch.name == 'instructor-commands').send('!begin-tests')

async def end_tests():
    await next(ch for ch in testing_bot.get_guild(TEST_GUILD_ID).text_channels if ch.name == 'instructor-commands').send('!end-tests')

if __name__ == '__main__':
    testing_bot.run(TOKEN)

def test_bot():
    testing_bot.run(TOKEN)
