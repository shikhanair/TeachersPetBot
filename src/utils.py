import asyncio

async def wait_for_msg(bot, channel):
    messages = await channel.history(limit=1).flatten()
    if messages[0].author.name != 'TeachersPetBot':
        return messages[0]
        
    # try:
    return await bot.wait_for('message', check=lambda x: x.guild.id == channel.guild.id)
    # except asyncio.TimeoutError:
        # messages = await channel.history(limit=1).flatten()
        # return messages[0]
