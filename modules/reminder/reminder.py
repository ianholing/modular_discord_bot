import asyncio

class Antonia:
    def __init__(self):
        pass

    async def on_ready(self, _client):
        self.client = _client
        self.client.loop.create_task(self.timer_reset_daily_tacos())

    async def timer_hourly_reminder(self):
        seconds_wait = 60 * 60
        print ("Waiting " + str(seconds_wait) + " to next reminder")
        await asyncio.sleep(seconds_wait)
        while True:
            await self.test_channel.send(f"TIME THINGS --> get_today: {time_utils.get_today()}    get_yesterday:{time_utils.get_yesterday()}  get_lastweek:{time_utils.get_lastweek()}    get_prevweek:{time_utils.get_prevweek()}    get_time_left:{time_utils.get_time_left()}  is_weekend:{time_utils.is_weekend()}")
            msg = use_cases.reset_daily_tacos()
            time_utils.update_time()
            await self.main_channel.send(msg)
            await asyncio.sleep(86400)
        pass

    async def on_message(self, client, message):
        if message.author == client.user:
            return

        # # RANDOM REPLIES
        # random_reply_counter -= 1
        # if random_reply_counter < 0:
        #     random_reply_counter = randint(5, 50)
        #     response = evaluateOneInput(message.content, model=self.generator)
        #     await message.channel.send(response)

        if client.user.mentioned_in(message):
            # response = evaluateOneInput(message.content, model=self.generator)
            #text = "User: " + message.content.split('> ')[1] + "\nBot:"
            input_text = message.content.split('> ')[1]
            print ("Infer with input: ", input_text)
            text = self.api_query(input_text)
            #response = text[0]['generated_text']
            response = text['generated_text']
            await message.channel.send(response)
            # loop =  asyncio.get_event_loop()
            # # task = loop.create_task(message.channel.send(response))
            # # loop.run_until_complete(task)
            # loop.run_until_complete(asyncio.gather(message.channel.send(response)))

            