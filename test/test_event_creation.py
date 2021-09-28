from utils import wait_for_msg

async def test_create_assignment_valid(testing_bot, commands_channel):
    async def wait(content):
        await wait_for_msg(testing_bot, commands_channel, content)

    await commands_channel.send('!create')
    await wait('Which type of event')

    await commands_channel.send('assignment')
    await wait('What would you like the assignment to be called')

    await commands_channel.send('test')
    await wait('Link associated with submission? Type N/A if none')

    await commands_channel.send('N/A')
    await wait('Extra description for assignment? Type N/A if none')

    await commands_channel.send('Some stuff')
    await wait('What is the due date')

    await commands_channel.send('01-01-1999')
    await wait('What time is this assignment due')

    await commands_channel.send('13:37')
    await wait('Assignment successfully created')


async def test_create_assignment_invalid_url(testing_bot, commands_channel):
    async def wait(content):
        await wait_for_msg(testing_bot, commands_channel, content)

    await commands_channel.send('!create')
    await wait('Which type of event')

    await commands_channel.send('assignment')
    await wait('What would you like the assignment to be called')

    await commands_channel.send('test')
    await wait('Link associated with submission? Type N/A if none')

    await commands_channel.send('Oops')
    await wait('Invalid URL. Aborting')


async def test_create_assignment_invalid_date(testing_bot, commands_channel):
    async def wait(content):
        await wait_for_msg(testing_bot, commands_channel, content)

    await commands_channel.send('!create')
    await wait('Which type of event')

    await commands_channel.send('assignment')
    await wait('What would you like the assignment to be called')

    await commands_channel.send('test')
    await wait('Link associated with submission? Type N/A if none')

    await commands_channel.send('N/A')
    await wait('Extra description for assignment? Type N/A if none')

    await commands_channel.send('Some stuff')
    await wait('What is the due date')

    await commands_channel.send('Oops')
    await wait('Invalid date')


async def test_create_assignment_invalid_time(testing_bot, commands_channel):
    async def wait(content):
        await wait_for_msg(testing_bot, commands_channel, content)

    await commands_channel.send('!create')
    await wait('Which type of event')

    await commands_channel.send('assignment')
    await wait('What would you like the assignment to be called')

    await commands_channel.send('test')
    await wait('Link associated with submission? Type N/A if none')

    await commands_channel.send('N/A')
    await wait('Extra description for assignment? Type N/A if none')

    await commands_channel.send('Some stuff')
    await wait('What is the due date')

    await commands_channel.send('01-01-1999')
    await wait('What time is this assignment due')

    await commands_channel.send('Oops')
    await wait('Incorrect input')


async def test_create_exam_valid(testing_bot, commands_channel):
    async def wait(content):
        await wait_for_msg(testing_bot, commands_channel, content)

    await commands_channel.send('!create')
    await wait('Which type of event')

    await commands_channel.send('exam')
    await wait('What is the title of this exam')

    await commands_channel.send('test')
    await wait('What content is this exam covering?')

    await commands_channel.send('Some stuff')
    await wait('What is the date of this exam?')

    await commands_channel.send('01-01-1999')
    await wait('Which times would you like the exam to be on')

    await commands_channel.send('12-12:01')
    await wait('Exam successfully created')


async def test_create_exam_invalid_date(testing_bot, commands_channel):
    async def wait(content):
        await wait_for_msg(testing_bot, commands_channel, content)

    await commands_channel.send('!create')
    await wait('Which type of event')

    await commands_channel.send('exam')
    await wait('What is the title of this exam')

    await commands_channel.send('test')
    await wait('What content is this exam covering?')

    await commands_channel.send('Some stuff')
    await wait('What is the date of this exam?')

    await commands_channel.send('Oops')
    await wait('Invalid date')


async def test_create_exam_invalid_time(testing_bot, commands_channel):
    async def wait(content):
        await wait_for_msg(testing_bot, commands_channel, content)

    await commands_channel.send('!create')
    await wait('Which type of event')

    await commands_channel.send('exam')
    await wait('What is the title of this exam')

    await commands_channel.send('test')
    await wait('What content is this exam covering?')

    await commands_channel.send('Some stuff')
    await wait('What is the date of this exam?')

    await commands_channel.send('01-01-1999')
    await wait('Which times would you like the exam to be on')

    await commands_channel.send('Oops')
    await wait('Incorrect input')


async def test_create_oh_valid(testing_bot, commands_channel):
    async def wait(content):
        await wait_for_msg(testing_bot, commands_channel, content)

    await commands_channel.send('!create')
    await wait('Which type of event')

    await commands_channel.send('office-hour')
    await wait('Which instructor will this office hour be for?')

    await commands_channel.send('Apollo')
    await wait('Which day would you like the office hour to be on')

    await commands_channel.send('Mon')
    await wait('Which times would you like the office hour to be on')

    await commands_channel.send('12-12:01')
    await wait('Office hour successfully created')


async def test_create_oh_invalid_times(testing_bot, commands_channel):
    async def wait(content):
        await wait_for_msg(testing_bot, commands_channel, content)

    await commands_channel.send('!create')
    await wait('Which type of event')

    await commands_channel.send('office-hour')
    await wait('Which instructor will this office hour be for?')

    await commands_channel.send('Apollo')
    await wait('Which day would you like the office hour to be on')

    await commands_channel.send('Mon')
    await wait('Which times would you like the office hour to be on')

    await commands_channel.send('Oops')
    await wait('Incorrect input')


async def test(testing_bot, guild_id):
    commands_channel = next(ch for ch in testing_bot.get_guild(guild_id).text_channels if ch.name == 'instructor-commands')
    await test_create_assignment_valid(testing_bot, commands_channel)
    await test_create_assignment_invalid_url(testing_bot, commands_channel)
    await test_create_assignment_invalid_date(testing_bot, commands_channel)
    await test_create_assignment_invalid_time(testing_bot, commands_channel)

    await test_create_exam_valid(testing_bot, commands_channel)
    await test_create_exam_invalid_date(testing_bot, commands_channel)
    await test_create_exam_invalid_time(testing_bot, commands_channel)

    await test_create_oh_valid(testing_bot, commands_channel)
    await test_create_oh_invalid_times(testing_bot, commands_channel)
