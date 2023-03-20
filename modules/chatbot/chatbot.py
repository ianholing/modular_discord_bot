import re
import openai
from random import randint
import functools
import typing
import asyncio
import utils.time_utils as time_utils
from config import MIN_RANDOM_REPLY_COUNTER, MAX_RANDOM_REPLY_COUNTER, CHATBOT_TOKEN, CHATBOT_ROLE, CHATBOT_NAME
from config import CHATBOT_METAROLE, CHATBOT_METAROLE_HELLO, SHOW_LEADERBOARD_CHANNEL, RESET_HOUR, CHATBOT_MODEL

def to_thread(func: typing.Callable) -> typing.Coroutine:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        return await asyncio.to_thread(func, *args, **kwargs)
    return wrapper

class Chatbot:
    random_reply_counter = randint(MIN_RANDOM_REPLY_COUNTER, MAX_RANDOM_REPLY_COUNTER)
    context_limit = 10
    context = []

    def __init__(self):
        openai.api_key = CHATBOT_TOKEN
        self.ACTUAL_ROLE = CHATBOT_ROLE
        pass

    async def on_ready(self, client):
        self.main_channel = await client.fetch_channel(SHOW_LEADERBOARD_CHANNEL)
        await self.update_role(greetings=False)
        client.loop.create_task(self.daily_role_change())

    async def update_role(self, greetings=True):
        # GET A NEW ROLE
        resp = openai.ChatCompletion.create(
            model=CHATBOT_MODEL,
            messages=[{'role': 'user', 'content': CHATBOT_METAROLE}]
        )
        self.ACTUAL_ROLE = resp.choices[0].message.content
        print("\n** NEW ROLE:", self.ACTUAL_ROLE)
        await asyncio.sleep(5)

        ## SAY HELLO WITH YOUR ROLE
        if greetings:
            messages = [{"role": "system", "content": self.ACTUAL_ROLE},
                        {'role': 'user', 'content': CHATBOT_METAROLE_HELLO}]
            resp = openai.ChatCompletion.create(
                model=CHATBOT_MODEL,
                messages=messages
            )

            txt_resp = resp.choices[0].message.content
            if resp.choices[0].message.content[:len(CHATBOT_NAME) + 2] == CHATBOT_NAME + ': ':
                txt_resp = txt_resp[len(CHATBOT_NAME) + 2:]

            await self.main_channel.send(txt_resp)

    async def daily_role_change(self):
        seconds_wait = time_utils.seconds_to(RESET_HOUR, 0) + 5
        await asyncio.sleep(seconds_wait)
        while True:
            print("\nChanging Role..")
            await self.update_role()
            await asyncio.sleep(86400)
        pass

    async def on_message(self, client, message):
        self.context.append({"role": "user", "content": message.author.name + ": " + self.parse_mentions(message.content.replace("\"", "\\\""), client)})
        self.context = self.context[-self.context_limit:]
        print("\nACTUAL CONTEXT:", self.context)
        if message.author == client.user:
            return

        # RANDOM REPLIES
        self.random_reply_counter -= 1
        if client.user.mentioned_in(message):
            response = await self.evaluate_input(message, client)
            await message.channel.send(response)
        elif self.random_reply_counter < 0:
            self.random_reply_counter = randint(MIN_RANDOM_REPLY_COUNTER, MAX_RANDOM_REPLY_COUNTER)
            print("\nNext random reply in", self.random_reply_counter, "messages")
            response = await self.evaluate_input(message, client, not_reply_on_fail=True)
            if len(response) > 0:
                await message.channel.send(response)

    def parse_mentions(self, input_text, client):
        parsed_text = input_text.replace('<@' + str(client.user.id) + '>', CHATBOT_NAME)
        matches = re.findall(r'\<@([A-Za-z0-9_]+)\>', parsed_text)
        for match in matches:
            print("\nMATCH:", match)
        return parsed_text

    @to_thread
    def evaluate_input(self, message, client, not_reply_on_fail=False):
        bot_input = self.parse_mentions(message.content.replace("\"", "\\\""), client)
        try:
            messages = [{"role": "system", "content": self.ACTUAL_ROLE}, *self.context]
            resp = openai.ChatCompletion.create(
                model=CHATBOT_MODEL,
                messages=messages
            )
        except:
            return 'Estoy saturado déjame vivir' 
        print(resp)
        txt_resp = resp.choices[0].message.content
        if resp.choices[0].message.content[:len(CHATBOT_NAME)+2] == CHATBOT_NAME + ': ':
            txt_resp = txt_resp[len(CHATBOT_NAME)+2:]
        return txt_resp
