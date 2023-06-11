import disnake
from disnake.ext import commands

import yaml
import os


config = yaml.safe_load(open("config.yml"))
slash_guilds = config.get("slash_guilds")
token = config.get("token")

client = commands.Bot(
    intents=disnake.Intents.all(),
    reload=True,
    test_guilds=slash_guilds
)


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


@client.event
async def on_ready():
    print(f"\nHere comes {client.user.name}!")
    await client.change_presence(
        activity=disnake.Activity(
            type=disnake.ActivityType.watching,
            name="Harm-Reduction"
        )
    )


client.run(token)
