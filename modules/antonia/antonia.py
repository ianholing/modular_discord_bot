from urllib import response

## HUGGING FACE
import json
import requests
from random import randint

from config import HUGGINGFACE_TOKEN, MIN_RANDOM_REPLY_COUNTER, MAX_RANDOM_REPLY_COUNTER

class Antonia:
    random_reply_counter = randint(MIN_RANDOM_REPLY_COUNTER, MAX_RANDOM_REPLY_COUNTER)

    def __init__(self):
        self.API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-3B"
        self.headers = {"Authorization": "Bearer " + HUGGINGFACE_TOKEN}

    def api_query(self, payload):
        data = json.dumps(payload)
        response = requests.request("POST", self.API_URL, headers=self.headers, data=data)
        print("RESPONSE: ", response)
        return json.loads(response.content.decode("utf-8"))

    async def on_message(self, client, message):
        if message.author == client.user:
            return

        # RANDOM REPLIES
        self.random_reply_counter -= 1
        if self.random_reply_counter < 0:
            self.random_reply_counter = randint(MIN_RANDOM_REPLY_COUNTER, MAX_RANDOM_REPLY_COUNTER)
            print ("Next random reply in", self.random_reply_counter, "messages")
            response = self.evaluate_input(message.content)
            await message.channel.send(response)
            return

        if client.user.mentioned_in(message):
            response = self.evaluate_input(message.content.split('> ')[1])
            await message.channel.send(response)

    def evaluate_input(self, input_text):
        # response = evaluateOneInput(message.content, model=self.generator)
        #text = "User: " + message.content.split('> ')[1] + "\nBot:"
        print ("Infer with input: ", input_text)
        text = self.api_query(input_text)
        #response = text[0]['generated_text']
        response = text['generated_text']
        return response
        # loop =  asyncio.get_event_loop()
        # # task = loop.create_task(message.channel.send(response))
        # # loop.run_until_complete(task)
        # loop.run_until_complete(asyncio.gather(message.channel.send(response)))
            