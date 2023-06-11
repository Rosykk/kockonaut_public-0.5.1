import disnake
from disnake.ext import commands
from disnake.ext.commands import Param
import yaml

config = yaml.safe_load(open("config.yml"))


class BreatheCog(commands.Cog):
    """breath command"""

    def __init__(self, client):
        self.client = client

    @commands.slash_command(name="breathe", description="Breathe command")
    async def _breathe(
            self,
            inter: disnake.ApplicationCommandInteraction,
            public: bool = Param(None, desc="Message")
    ):
        res = 'https://i.imgur.com/XMLJaQM.gif'

        if public:
            return await inter.response.send_message(content=res)

        return await inter.response.send_message(content=res, ephemeral=True)


def setup(client):
    client.add_cog(BreatheCog(client))
