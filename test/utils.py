import asyncio
from time import sleep

async def wait_for_msg(testing_bot, channel, content):
    sleep(0.6)
    try:
        return await testing_bot.wait_for('message', timeout=2, check=lambda x: x.guild.id == channel.guild.id and x.author.name == 'TeachersPetBot' and content in x.content)
    except asyncio.TimeoutError:
        messages = await channel.history(limit=1).flatten()
        if not (len(messages) != 0 and content in messages[0].content):
            print(f'Message content {content} not found')
            raise Exception()
        return messages[0]


async def wait_for_channel_create(testing_bot, guild_id, name):
    try:
        return await testing_bot.wait_for('guild_channel_create', timeout=2, check=lambda x: x.guild.id == guild_id and x.name == name)
    except asyncio.TimeoutError:
        new_channel = next((ch for ch in testing_bot.get_guild(guild_id).text_channels if ch.name == name), None)
        if new_channel is None:
            print(f'Channel {name} not found')
            raise Exception()
        return new_channel
