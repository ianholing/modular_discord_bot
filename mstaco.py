import re

from emoji.core import emoji_lis
import use_cases

from config import TACO
import emoji
from config import SHOW_LEADERBOARD_CHANNEL, TEST_CHANNEL, RESET_HOUR
import asyncio


import time_utils

class Mstaco:
    def __init__(self):
        pass

    async def on_ready(self, _client):
        self.client = _client
        self.test_channel = await self.client.fetch_channel(TEST_CHANNEL)
        self.main_channel = await self.client.fetch_channel(SHOW_LEADERBOARD_CHANNEL)
        self.client.loop.create_task(self.timer_reset_daily_tacos())

    async def timer_reset_daily_tacos(self):
        seconds_wait = time_utils.seconds_to(RESET_HOUR,0)
        print ("Waiting " + str(seconds_wait) + " to reset tacos message")
        await asyncio.sleep(seconds_wait)
        while True:
            await self.test_channel.send(f"TIME THINGS --> get_today: {time_utils.get_today()}    get_yesterday:{time_utils.get_yesterday()}  get_lastweek:{time_utils.get_lastweek()}    get_prevweek:{time_utils.get_prevweek()}    get_time_left:{time_utils.get_time_left()}  is_weekend:{time_utils.is_weekend()}")
            msg = use_cases.reset_daily_tacos()
            time_utils.update_time()
            await self.main_channel.send(msg)
            await asyncio.sleep(86400)
        pass

    # event handlers
    async def handle_daily_bonus(self, client, message):
        if message.author is not client.user:
            msg = use_cases.give_bonus_taco_if_required(message.author.id)
            if msg is not None:
                await message.author.send(msg)


    async def handle_message(self, client, message):
        given_tacos = 0
        emoji_list = emoji.emoji_lis(message.content)

        for _emoji in emoji_list:
            emoji_name = emoji.demojize(_emoji['emoji'])

            if emoji_name in TACO:
                print ("TACOS PARTY:", TACO[emoji_name])
                given_tacos = given_tacos + TACO[emoji_name]

        print ("GIVED TACOS", given_tacos)
        if given_tacos == 0:
            return

        giver = message.author
        for mention in message.mentions:
            receiver = mention
            if giver == receiver:
                continue

            if len(emoji_list) > 1:
                giver_message, receiver_message = use_cases.give_tacos(giver.id, receiver.id, given_tacos, False, message.channel.id)
            else:
                giver_message, receiver_message = use_cases.give_tacos(giver.id, receiver.id, given_tacos, False, message.channel.id, emoji_list[0]['emoji'])

            if giver_message is not None:
                await giver.send(giver_message)
                
            if receiver_message is not None:
                await receiver.send(receiver_message)

        return True


    async def handle_reaction(self, client, payload):
        if payload.event_type == 'REACTION_ADD':
            emoji_name = emoji.demojize(payload.emoji.name)
            print ("REACTION:", emoji_name, payload)

            if emoji_name in TACO:
                print ("TACOS PARTY:", TACO[emoji_name])

                channel = await client.fetch_channel(payload.channel_id)
                message = await channel.fetch_message(payload.message_id)
                giver = payload.member
                receiver = message.author
                if giver == receiver:
                    return
                given_tacos = TACO[emoji_name]
                giver_message, receiver_message = use_cases.give_tacos(giver.id, receiver.id, given_tacos, True, payload.channel_id, payload.emoji)

                if giver_message is not None:
                    await giver.send(giver_message)
                
                if receiver_message is not None:
                    await receiver.send(receiver_message)



    async def handle_direct_command(self, client, message):
        clean = re.compile('<@!.*?>')
        command = re.sub(clean, '', message.content).strip()
        if command == '/leaderboard':
            msg = use_cases.print_leaderboard()
            await message.channel.send(msg)
            return True

        if command == '/leaderboard_me':
            msg = use_cases.print_leaderboard_me(message.author)
            await message.channel.send(msg)
            return True

        if command == '/weeklyleaderboard':
            msg = use_cases.print_weekly_leaderboard()
            await message.channel.send(msg)
            return True

    async def on_message(self, client, message):
        if message.author == client.user:
            return

        if client.user.mentioned_in(message):
            return await self.handle_direct_command(client, message)
        else:
            await self.handle_daily_bonus(client, message)
            return await self.handle_message(client, message)

    async def on_raw_reaction_add(self, client, payload):
        await self.handle_reaction(client, payload)

            