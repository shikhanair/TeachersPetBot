async def get_queue(testing_bot):
    bot_queue_resp = await testing_bot.wait_for('message', check=lambda m: 'Queue' in m.content)
    return bot_queue_resp.content.split('\n')[2:]

async def test_oh_queue_individ(testing_bot, guild_id):
    await testing_bot.wait_for('guild_channel_create', timeout=3)
    oh_channel = next((ch for ch in testing_bot.get_guild(guild_id).text_channels if 'office-hour-test' in ch.name), None)
    if not oh_channel:
        assert False
    await oh_channel.send('!oh enter')

    queue = await get_queue(testing_bot)
    assert len(queue) == 1 and 'TeachersPetBotTester' in queue[0]

    await oh_channel.send('!oh exit')

    queue = await get_queue(testing_bot)
    assert queue[0] == '(The queue is currently empty)'

async def test(testing_bot, guild_id):
    await test_oh_queue_individ(testing_bot, guild_id)