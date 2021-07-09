from dis import disco
import os
from discord.ext import tasks

import discord
from discord.ext import commands
from config import DISCORD_TOKEN

# MODULES
import mstaco
import antonia

# import nest_asyncio
# nest_asyncio.apply()
# __import__('IPython').embed()

class Metadonia:
    def __init__(self):
        self.client = discord.Client()
        self.bot = commands.Bot(command_prefix='!')
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

discord = Metadonia()
discord.add_ready_listener(on_ready_logger)
discord.add_message_listener(on_message_logger)
discord.add_module(mstaco.Mstaco())
discord.add_module(antonia.Antonia())
discord.start()
