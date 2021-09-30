###########################
# Tests Event creation & calendar functionality
###########################
import discord
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
    
async def test(testing_bot, guild_id):
    print('testing calendar')
    
    guild = testing_bot.get_guild(guild_id)    

    flag = False
    for channel in guild.text_channels:
        if(channel.name == 'course-calendar'):
            flag = True

    assert flag
    
    print('testing calendar embed')
    
    course_calendar = discord.utils.get(testing_bot.get_all_channels(), name='course-calendar')

