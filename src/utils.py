from time import sleep

async def wait_for_msg(bot, channel):
    messages = await channel.history(limit=1).flatten()
    if messages[0].author.name != 'TeachersPetBot':
        sleep(0.25)
        return messages[0]

    # try:
    msg = await bot.wait_for('message', check=lambda x: x.guild.id == channel.guild.id)
    sleep(0.25)
    return msg
    # except asyncio.TimeoutError:
        # messages = await channel.history(limit=1).flatten()
        # return messages[0]
