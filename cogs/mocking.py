import disnake
from disnake.ext import commands
from disnake.ext.commands import Param
import yaml

config = yaml.safe_load(open("config.yml"))


class MockingCog(commands.Cog):
    """mocking command"""

    def __init__(self, client):
        self.client = client

    @commands.slash_command(name="mock", description="Mocking command")
    async def _mock_cog(
            self,
            inter: disnake.ApplicationCommandInteraction,
            text: str = Param(..., desc="Message")
    ):

        res = "".join([ele.upper() if not idx % 2 else ele.lower() for idx, ele in enumerate(text)])

        return await inter.response.send_message(res, ephemeral=True)


def setup(client):
    client.add_cog(MockingCog(client))
