async def get_queue(testing_bot):
    bot_queue_resp = await testing_bot.wait_for('message', check=lambda m: 'Queue' in m.content)
    return bot_queue_resp.content.split('\n')[2:]


async def test_oh_queue_individ(testing_bot, oh_channel):
    await oh_channel.send('!oh enter')

    queue = await get_queue(testing_bot)
    assert len(queue) == 1 and 'TeachersPetBotTester' in queue[0]

    await oh_channel.send('!oh exit')

    queue = await get_queue(testing_bot)
    assert queue[0] == '(The queue is currently empty)'


async def test_oh_advance(testing_bot, oh_channel):
    await oh_channel.send('!oh enter')

    queue = await get_queue(testing_bot)
    assert len(queue) == 1 and 'TeachersPetBotTester' in queue[0]

    role = next(r for r in testing_bot.guild.roles if r.name == 'Instructor')
    await testing_bot.user.add_roles(role)

    await oh_channel.send('!oh next')

    queue = await get_queue(testing_bot)
    assert queue[0] == '(The queue is currently empty)'

    await testing_bot.user.remove_roles(role)


async def test(testing_bot, guild_id):
    oh_channel = await testing_bot.wait_for('guild_channel_create', timeout=3, check=lambda x: x.guild.id == guild_id and 'office-hour-test' in x.name)
    await testing_bot.wait_for('message', timeout=3, check=lambda x: x.guild.id == guild_id and 'TeachersPetBot' in x.author.name and "Welcome to test's office hour!" in x.content)

    await test_oh_queue_individ(testing_bot, oh_channel)