import asyncio

from config import SHOW_PARROT_CHANNEL, TEST_CHANNEL

class Parrot:
    def __init__(self):
        pass

    async def on_ready(self, _client):
        self.client = _client
        self.test_channel = await self.client.fetch_channel(TEST_CHANNEL)
        self.main_channel = await self.client.fetch_channel(SHOW_PARROT_CHANNEL)

    async def on_message(self, client, message):
        if message.author == client.user:
            return
        
        # IS TRIGGER
        msg = message.content
        tmp = message.content.split('> ')
        if len(tmp) > 1:
            msg = ' '.join(tmp[1:]).strip()
        if msg.lower().startswith('repeat'):
            msg = self.remove_prefix(msg, 'repeat ').strip()

            #channel = discord.utils.get(ctx.guild.channels, name=given_name)
            if msg.lower().startswith('test channel'):
                await self.test_channel.send(msg)
            else:
                await self.main_channel.send(msg)
            return True

    def remove_prefix(self, s, prefix):
        return s[len(prefix):] if s.startswith(prefix) else s