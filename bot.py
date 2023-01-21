import discord
from config import DISCORD_TOKEN

# MODULES
import modules.mstaco.mstaco as mstaco
import modules.chatbot.chatbot as chatbot
import modules.reminder.reminder as reminder
import modules.parrot.parrot as parrot

class Metabot:
    def __init__(self):
        self.client = discord.Client(intents=discord.Intents.all())
        self.on_ready = self.client.event(self.on_ready)
        self.on_message = self.client.event(self.on_message)
        self.on_raw_reaction_add = self.client.event(self.on_raw_reaction_add)
        self.on_ready_listeners = []
        self.on_message_listeners = []
        self.on_reaction_add_listeners = []

    def add_module(self, module):
        if hasattr(module, 'on_ready'):
            self.add_ready_listener(module.on_ready)

        if hasattr(module, 'on_message'):
            self.add_message_listener(module.on_message)

        if hasattr(module, 'on_raw_reaction_add'):
            self.add_on_reaction_add_listeners(module.on_raw_reaction_add)

    def add_ready_listener(self, callback):
        self.on_ready_listeners.append(callback)

    def add_message_listener(self, callback):
        self.on_message_listeners.append(callback)

    def add_on_reaction_add_listeners(self, callback):
        self.on_reaction_add_listeners.append(callback)

    async def on_ready(self):
        for callback in self.on_ready_listeners:
            await callback(self.client)

    async def on_message(self, message):
        for callback in self.on_message_listeners:
            if await callback(self.client, message):
                break

    async def on_raw_reaction_add(self, payload):
        for callback in self.on_reaction_add_listeners:
            await callback(self.client, payload)

    def start(self):
        self.client.run(DISCORD_TOKEN)


async def on_ready_logger(client):
    print(f'{client.user.name} has connected to Discord!')

async def on_message_logger(client, message):
    print(f'Message \"{message.content}\" FROM: {message.author}')

discord = Metabot()
discord.add_ready_listener(on_ready_logger)
discord.add_message_listener(on_message_logger)
discord.add_module(mstaco.Mstaco())
discord.add_module(parrot.Parrot())
discord.add_module(reminder.Reminder())
discord.add_module(chatbot.Chatbot())
discord.start()