import asyncio
import utils.time_utils as time_utils
from config import MIN_REMINDER_TIME, SKIP_LEADERBOARD_WEEKEND, TEST_CHANNEL, SHOW_REMINDER_CHANNEL

class Reminder:
    def __init__(self):
        pass

    async def on_ready(self, _client):
        self.client = _client
        self.test_channel = await self.client.fetch_channel(TEST_CHANNEL)
        self.main_channel = await self.client.fetch_channel(SHOW_REMINDER_CHANNEL)
        self.client.loop.create_task(self.timer_hourly_reminder())

    async def timer_hourly_reminder(self):
        print ("Waiting " + str(MIN_REMINDER_TIME) + " to next reminder")
        await asyncio.sleep(MIN_REMINDER_TIME)
        while True:
            if not (SKIP_LEADERBOARD_WEEKEND and time_utils.is_weekend()):
                await self.test_channel.send(f"Remind wait for {MIN_REMINDER_TIME}")
            #await self.main_channel.send(msg)
            await asyncio.sleep(MIN_REMINDER_TIME)
        pass

    async def on_message(self, client, message):
        pass

            