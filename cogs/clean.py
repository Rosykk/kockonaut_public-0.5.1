import disnake
from disnake.ext import commands
from disnake.ext.commands import Param
import yaml

config = yaml.safe_load(open("config.yml"))


class CleanCommand(commands.Cog):
    """clean command"""

    def __init__(self, client):
        self.client = client

    @commands.slash_command(name="clean", description="Clean command")
    async def _breathe(
            self,
            inter: disnake.ApplicationCommandInteraction,
            amount: int = Param(None, desc="How many messages to delete")
    ):
        await inter.response.defer()

        if amount is None:
            return await inter.response.send_message(content="Please specify amount of messages to delete", ephemeral=True)

        if amount > 1000:
            return await inter.response.send_message(content="You can't delete more than 1000 messages", ephemeral=True)

        await inter.channel.purge(limit=amount + 1)


def setup(client):
    client.add_cog(CleanCommand(client))
