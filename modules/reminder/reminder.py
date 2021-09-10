import asyncio
import utils.time_utils as time_utils
from config import MIN_REMINDER_TIME, SKIP_LEADERBOARD_WEEKEND, TEST_CHANNEL, SHOW_REMINDER_CHANNEL, HELP_TEXT

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
            #if not (SKIP_LEADERBOARD_WEEKEND and time_utils.is_weekend()):
            #    await self.test_channel.send(f"Remind wait for {MIN_REMINDER_TIME}")
            #await self.main_channel.send(msg)
            await asyncio.sleep(MIN_REMINDER_TIME)
        pass

    async def on_message(self, client, message):
        if message.author == client.user:
            return
        
        # IS TRIGGER
        msg = message.content
        tmp = message.content.split('> ')
        print (len(tmp))
        if len(tmp) > 1:
            msg = ' '.join(tmp[1:]).strip()
        if msg.lower().startswith('recuerda'):
            msg = self.remove_prefix(msg, 'recuerda a ').strip()
            msg = self.remove_prefix(msg, 'recuerda ').strip()

            # IS HELP
            if msg.startswith('help') or msg.startswith('ayuda'):
                await message.channel.send(HELP_TEXT)
                return True

            print ("RECUERDA MESSAGE: ", msg)
            fields = msg.split(",")

            ## PARSEAR CAMPOS
            ## CREAR RECUERDO
            ## DEVOLVER MENSAJE: "TU RECUERDO SE HA CREADO CON EL ID XXXXX"
            return True

    def remove_prefix(self, s, prefix):
        return s[len(prefix):] if s.startswith(prefix) else s