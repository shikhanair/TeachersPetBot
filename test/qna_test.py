# import pytest
# import discord.ext.test as test
# import discord
# import discord.ext.commands as commands
#
#
# @pytest.fixture
# def client(event_loop):
#     intents = discord.Intents.all()
#     c = commands.Bot(intents=intents, command_prefix='!', loop=event_loop)
#     # c = discord.Client(loop=event_loop)
#     test.configure(c)
#
#     @c.command()
#     async def hello(ctx):
#         await ctx.send('test successful')
#
#     return c
#
# @pytest.mark.asyncio
# async def test_dm_send(client):
#     # guild = client.guilds[0]
#     # print(guild)
#     # await guild.members[0].send("hi")
#
#     await test.message('!hello')
#     assert test.verify().message().contains().content("test successful")


import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from time import sleep

load_dotenv()
TOKEN = os.getenv('TESTING_BOT_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

testing_bot = discord.Client()


@testing_bot.event
async def on_ready():
    print('Testing bot running for Q and A')
    print('------')
    await test_qna()


async def test_qna():
    qna_channel = discord.utils.get(testing_bot.get_all_channels(), name='q-and-a')
    await qna_channel.send('!ask \"Hello\"')

    sleep(0.5)

    messages = await qna_channel.history(limit=1).flatten()
    for m in messages:
        print(m.content)
        assert 'Hello' in m.content


testing_bot.run(TOKEN)
