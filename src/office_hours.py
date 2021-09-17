# Office hours related features
import datetime
import schedule
import discord

class Group:
    def __init__(self, student, group_id):
        self.group_members = [student]
        self.group_id = group_id

class OfficeHourQueue:
    def __init__(self, ta_name, text_channel, voice_channel, waiting_room):
        self.current_student = None
        self.queue = []
        self.prev_queue_message = None
        self.ta_name = ta_name
        self.text_channel = text_channel
        self.voice_channel = voice_channel
        self.waiting_room = waiting_room
        self.next_grp_id = 0
    
    def enqueue(self, student):
        self.queue.append(Group(student, '{:03d}'.format(self.next_grp_id)))
        self.next_grp_id = (self.next_grp_id + 1) % 1000

office_hour_queues = {}

async def display_queue(office_hour_queue):
    if office_hour_queue.prev_queue_message:
        await office_hour_queue.prev_queue_message.delete()

    queue_str = (
        'Office Hour Queue:\n'
        '------------------\n' +
        '\n'.join(
            f"{i + 1}: {', '.join(grp.group_members)} (group ID: {grp.group_id})"
            for i, grp
            in enumerate(office_hour_queue.queue)
        )
    )
    office_hour_queue.prev_queue_message = await office_hour_queue.text_channel.send(queue_str)


def get_office_hour_times(calendar):
    # TODO
    return (datetime.datetime(2021, 11, 11, 5, 12, 10), datetime.datetime(2021, 11, 11, 5, 12, 10))

    # .send(queue_str)

# TODO waiting list

async def office_hour_command(ctx, command, *args):
    if ctx.channel.name[:len('office-hour-')] == 'office-hour-':
        ta = ctx.channel.name[len('office-hour-'):]

        office_hour_queue = office_hour_queues[ta]
        queue = office_hour_queue.queue

        if command == 'enter' and 'Student' in ctx.author.roles:
            all_queued_students = []
            for (group_members, _) in queue:
                all_queued_students.append(*group_members)
            if ctx.author.name not in all_queued_students:
                if len(args) == 0:
                    office_hour_queue.enqueue(ctx.author)
                    await display_queue(ctx.channel)
                elif len(args) == 1:
                    group_id_to_join = args[0]
                    group_to_join = next((group for group in queue if group_id_to_join == group.group_id), None)
                    if group_to_join:
                        # TODO maybe implement in future
                        # for member in group_to_join.group_members:
                        #     message = (f'{ctx.author.name} {f"(nickname: {ctx.author.nick})" if ctx.author.nick != ctx.author.name else ""} '
                        #         'is attempting to join your office hour group. Replay with `!oh group accept` to accept or `!oh group reject` to reject this student.')
                        #     await member.send(message)
                        queue.group_members.append(ctx.author)
                        await display_queue(ctx.channel)
                    else:
                        await ctx.author.send(
                            'The office hour group you have attempted to join does not exist. '
                            'Please ensure you enter a valid group ID when attempting to join an office hour group.'
                        )
                await office_hour_queue.waiting_room.set_permissions(ctx.author, read_messages=True, send_messages=True)
            else:
                await ctx.author.send(
                    'You are already in the office hour queue so you cannot join again. '
                    'If you would like to join an office hour group, please exit the queue and join the group.'
                )
        elif command == 'exit' and 'Student' in ctx.author.roles:
            queued_group = next((group for group in queue if ctx.author in group.group_members), None)
            if queued_group:
                queued_group.group_members.remove(ctx.author)
                if len(queued_group.group_members) == 0:
                    queue.remove(queued_group)
                await office_hour_queue.waiting_room.set_permissions(ctx.author, read_messages=True, send_messages=True)
                await display_queue(ctx.channel)
        elif command == 'next' and 'Instructor' in ctx.author.roles:
            voice_channel = office_hour_queue.voice_channel
            waiting_room = office_hour_queue.waiting_room

            if office_hour_queue.current_student:
                await voice_channel.set_permissions(office_hour_queue.current_student, overwrite=None)
                await waiting_room.set_permissions(office_hour_queue.current_student, overwrite=None)

            next_group = queue.pop(0)
            for member in next_group.group_members:
                await voice_channel.set_permissions(member, read_messages=True, send_messages=True)
                await waiting_room.set_permissions(member, read_messages=True, send_messages=True)

                message = f"{office_hour_queue.ta_name} is ready to help {'you' if len(next_group.group_members) == 1 else 'your group'}. Please join the office hour voice channel."
                await member.send(message)
    else:
        await ctx.author.send('The `!oh` command is only valid in office hour text channels.')

    await ctx.message.delete()


async def open_oh(guild, ta):
    category = await guild.create_category_channel(f'Office Hour {ta}')

    instructor_role = next((role for role in guild.roles if role.name == 'Instructor'), None)
    overwrites = {
        instructor_role: discord.PermissionOverwrite(read_messages=True, send_messages=True)
    }

    ta_name_channelified = ta.lower().replace(" ", "-")
    text_channel = await category.create_text_channel(f'office-hour-{ta_name_channelified}')
    voice_channel = await category.create_voice_channel(f'office-hour-{ta_name_channelified}', overwrites=overwrites)
    waiting_room = await category.create_voice_channel(f'office-hour-{ta_name_channelified}-waiting-list', overwrites=overwrites)

    await text_channel.send(
        f"Welcome to {ta}'s office hour!\n"
        'To join the queue, please type `!oh enter` in this channel. '
        'If you would like to join an existing office hour group, type `!oh enter <groupID>\n`'
        'If you would like to exit the queue, please type `!oh exit`.\n'
        f'You may join the waiting list channel (office-hour-{ta_name_channelified}-waiting-list)'
        "while you wait for your turn if you'd like. When it is your turn, you will be notified."
    )

    office_hour_queues[ta_name_channelified] = OfficeHourQueue(ta, text_channel, voice_channel, waiting_room)


async def close_oh(guild, ta):
    channel_category = next((cat for cat in guild.categories if cat.name == f'Office Hour {ta}'), None)
    await channel_category.delete()
    ta_name_channelified = ta.lower().replace(" ", "-")
    office_hour_queues.pop(ta_name_channelified)
    # ta_name_channelified = ta.lower().replace(" ", "-")
    # channels_to_delete = [
    #     next((chan for chan in guild.text_channels if chan.name == f'office-hour-{ta_name_channelified}'), None),
    #     next((chan for chan in guild.voice_channels if chan.name == f'office-hour-{ta_name_channelified}'), None),
    #     next((chan for chan in guild.voice_channels if chan.name == f'office-hour-{ta_name_channelified}-waiting-list'), None)
    # ]
    # for channel in channels_to_delete:
    #     if channel:
    #         await channel.delete()


class TaOfficeHour:
    def __init__(self, ta, times):
        self.ta = ta
        self.times = times


def init(bot):
    for guild in bot.guilds:
        ta_office_hours = [
            TaOfficeHour('Alex', (datetime.datetime(2021, 11, 11, 5, 12, 10), datetime.datetime(2021, 11, 11, 5, 12, 10)))
        ]
        for office_hour in ta_office_hours:
            begin_time, end_time = (t.strftime('%H:%M') for t in office_hour.times)
            schedule.every().day.at(begin_time).do(open_oh, guild=guild, ta=office_hour.ta)
            schedule.every().day.at(end_time).do(close_oh, guild=guild, ta=office_hour.ta)