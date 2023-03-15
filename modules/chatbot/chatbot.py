from urllib import response

## HUGGING FACE
import re
from chatgpt_wrapper import ChatGPT
import subprocess
from random import randint

from config import HUGGINGFACE_TOKEN, MIN_RANDOM_REPLY_COUNTER, MAX_RANDOM_REPLY_COUNTER

class Chatbot:
    random_reply_counter = randint(MIN_RANDOM_REPLY_COUNTER, MAX_RANDOM_REPLY_COUNTER)

    def __init__(self):
        pass

    async def on_message(self, client, message):
        if message.author == client.user:
            return

        # RANDOM REPLIES
        self.random_reply_counter -= 1
        if self.random_reply_counter < 0:
            self.random_reply_counter = randint(MIN_RANDOM_REPLY_COUNTER, MAX_RANDOM_REPLY_COUNTER)
            print("Next random reply in", self.random_reply_counter, "messages")
            response = self.evaluate_input(message.content, client)
            await message.channel.send(response)
            return

        if client.user.mentioned_in(message):
            response = self.evaluate_input(message.content, client)
            await message.channel.send(response)

    def parse_mentions(self, input_text, client):
        parsed_text = input_text.replace('<@'+str(client.user.id)+'>', "ChatGPT")
        matches = re.findall(r'\<@([A-Za-z0-9_]+)\>', parsed_text)
        for match in matches:
            print("MATCH:", match)
        return parsed_text

    def evaluate_input(self, input_text, client):
        bot_input = self.parse_mentions(input_text, client)
        # bot = ChatGPT()
        # return bot.ask(bot_input)

        p = subprocess.Popen('timeout 60 chatgpt ' + bot_input, shell=True, stdout=subprocess.PIPE)
        p.wait()
        if p.returncode == 0:
            resp = []
            for line in p.stdout:
                if len(line) > 1:
                    resp.append(line.decode('utf-8'))
            return ' '.join(resp)
        else:
                return 'Estoy saturado dejarme vivir'
            