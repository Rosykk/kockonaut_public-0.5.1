import disnake
import yaml
from disnake.ext import commands

config = yaml.safe_load(open("config.yml"))
introduce_ch = config.get("introduce_channel")
welcome_ch = config.get("welcome_channel")
system_ch = config.get("system_channel")


class OnMemberQuitJoin(commands.Cog):
    def __init__(self, client):
        """Waits for a message and posts an embed on server boost."""
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.bot:
            return

        room = self.client.get_channel(introduce_ch)

        await self.client.get_channel(welcome_ch).send(f"🟢 **»** {member.mention} se připojil na server! Vítej! Pokud se nám chceš představit, můžeš použít {room.mention}!")
        await self.client.get_channel(system_ch).send(f"🟢 **»** {member.mention} se **připojil** na server.")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if member.bot:
            return

        username = str(member)

        view = disnake.ui.View()
        view.add_item(disnake.ui.Button(label=str(username), url=f"discord://-/users/{member.id}"))

        await self.client.get_channel(system_ch).send(f"🔴 **»** {username} **({member.id})** se **odpojil** ze serveru.", view=view)


def setup(client):
    client.add_cog(OnMemberQuitJoin(client))
