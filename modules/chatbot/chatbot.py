import re
import openai
from random import randint
import functools
import typing
import asyncio

from config import MIN_RANDOM_REPLY_COUNTER, MAX_RANDOM_REPLY_COUNTER, CHATBOT_TOKEN, CHATBOT_ROLE, CHATBOT_NAME

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
        pass

    async def on_message(self, client, message):
        self.context.append({"role": "user", "content": message.author.name + ": " + self.parse_mentions(message.content.replace("\"", "\\\""), client)})
        self.context = self.context[-self.context_limit:]
        print("ACTUAL CONTEXT:", self.context)
        if message.author == client.user:
            return

        # RANDOM REPLIES
        self.random_reply_counter -= 1
        if client.user.mentioned_in(message):
            response = await self.evaluate_input(message, client)
            await message.channel.send(response)
        elif self.random_reply_counter < 0:
            self.random_reply_counter = randint(MIN_RANDOM_REPLY_COUNTER, MAX_RANDOM_REPLY_COUNTER)
            print("Next random reply in", self.random_reply_counter, "messages")
            response = await self.evaluate_input(message, client, not_reply_on_fail=True)
            if len(response) > 0:
                await message.channel.send(response)

    def parse_mentions(self, input_text, client):
        parsed_text = input_text.replace('<@' + str(client.user.id) + '>', CHATBOT_NAME)
        matches = re.findall(r'\<@([A-Za-z0-9_]+)\>', parsed_text)
        for match in matches:
            print("MATCH:", match)
        return parsed_text

    @to_thread
    def evaluate_input(self, message, client, not_reply_on_fail=False):
        bot_input = self.parse_mentions(message.content.replace("\"", "\\\""), client)
        try:
            messages = [{"role": "system", "content": CHATBOT_ROLE}, *self.context]
            resp = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
        except:
            return 'Estoy saturado déjame vivir' 
        print(resp)
        txt_resp = resp.choices[0].message.content
        if resp.choices[0].message.content[:len(CHATBOT_NAME)+2] == CHATBOT_NAME + ': ':
            txt_resp = txt_resp[len(CHATBOT_NAME)+2:]
        return txt_resp
