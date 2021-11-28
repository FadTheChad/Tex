import discord

import importlib.util

import json

import os
from os.path import join

from typing import Dict

class TXClient(discord.Client):
    commands: Dict[str] = {}
    events: Dict[str] = {}

    def __init__(self, **options):
        super().__init__(**options)
        print('Starting Bot...')

    def activate(self):
        event_dir = os.getcwd() + '\\src\\events'

        event_files = [join(event_dir, f) for f in os.listdir(event_dir) if f.endswith('.py')]

        with open('config.json') as file:
            config = json.load(file)

        for event_file in event_files:
            spec = importlib.util.spec_from_file_location("event", event_file)
            event_module = importlib.util.module_from_spec(spec)

            spec.loader.exec_module(event_module)
            event = getattr(event_module, 'event')

            self.events[event['name']] = event['run']

        @self.event
        async def on_ready():
            await self.events['on_ready']()

        @self.event
        async def on_message(message):
            await self.events['on_message'](message)

        self.run(config['token'])