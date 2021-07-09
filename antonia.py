from urllib import response

## HUGGING FACE
import json
import requests
import asyncio

from config import HUGGINGFACE_TOKEN

#random_reply_counter = randint(5, 50)

class Antonia:
    def __init__(self):
        self.API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-3B"
        self.headers = {"Authorization": "Bearer " + HUGGINGFACE_TOKEN}

    def api_query(self, payload):
        data = json.dumps(payload)
        response = requests.request("POST", self.API_URL, headers=self.headers, data=data)
        return json.loads(response.content.decode("utf-8"))

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

            