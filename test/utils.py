import asyncio

async def wait_for_msg(testing_bot, channel, content):
    try:
        return await testing_bot.wait_for('message', timeout=2, check=lambda x: x.guild.id == channel.guild.id and x.author.name == 'TeachersPetBot' and content in x.content)
    except asyncio.TimeoutError:
        messages = await channel.history(limit=1).flatten()
        assert len(messages) != 0 and content in messages[0].content
        return messages[0]