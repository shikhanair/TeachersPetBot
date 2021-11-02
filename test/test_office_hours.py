from utils import wait_for_msg, wait_for_channel_create

async def get_queue(testing_bot, oh_channel):
    bot_queue_resp = await wait_for_msg(testing_bot, oh_channel, 'Queue')

    return bot_queue_resp.content.split('\n')[2:]


async def test_oh_queue_individ(testing_bot, oh_channel):
    await oh_channel.send('!oh enter')

    queue = await get_queue(testing_bot, oh_channel)

    assert len(queue) == 1 and testing_bot.user.name in queue[0]
    
    await oh_channel.send('!oh exit')

    queue = await get_queue(testing_bot, oh_channel)
    assert queue[0] == '(The queue is currently empty)'


async def test(testing_bot, guild_id):
    oh_channel = await wait_for_channel_create(testing_bot, guild_id, 'office-hour-test')

    await wait_for_msg(testing_bot, oh_channel, "Welcome to test's office hour!")

    await test_oh_queue_individ(testing_bot, oh_channel)
