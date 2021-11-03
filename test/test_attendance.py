###########################
# Tests attendance functionality
###########################
from time import sleep
import discord


async def test(testing_bot, guild_id):
    commands_channel = discord.utils.get(testing_bot.get_all_channels(),
                                         name='instructor-commands')
    guild = testing_bot.get_guild(guild_id)
    role = discord.utils.get(guild.roles,
                             name="Instructor")

    member = guild.get_member(testing_bot.user.id)
    await member.add_roles(role)

    print('testing attendance')
    await commands_channel.send('!attendance')
    sleep(3)
    messages = await commands_channel.history(limit=1).flatten()
    assert messages.__class__ == list

    commands_channel = discord.utils.get(testing_bot.get_all_channels(),
                                         name='q-and-a')
    await commands_channel.send('!attendance')
    sleep(3)
    messages = await commands_channel.history(limit=1).flatten()
    for message in messages:
        assert 'Command runs only in the instructor-commands channel' in message.content
    await member.remove_roles(role)
