import disnake
from disnake.ext import commands
from disnake.ext.commands import Param
from functions.firebase import db
from datetime import datetime
import yaml
import time

config = yaml.safe_load(open("config.yml"))
warn_ch = config.get("report_channel")
roles = config.get("report_roles")


class ReportCog(commands.Cog):
    """report command"""

    def __init__(self, client):
        self.client = client
        self.report_cooldown = 30 * 60
        self.last_reports = {}

    # * list unpacking     \/
    @commands.has_any_role(*roles)
    @commands.slash_command(name="report", description="Report command")
    async def _report(
            self,
            inter: disnake.ApplicationCommandInteraction,
            user: disnake.Member = Param(..., desc="Username"),
            reason: str = Param(..., desc="Reason")
    ):
        last_report_ts = self.last_reports.get(user.id, (time.time() - self.report_cooldown))
        if (time.time() - last_report_ts) < self.report_cooldown:
            return await inter.response.send_message(f"Ještě neuběhlo {int(self.report_cooldown / 60)} minut od posledního reportu! (<t:{int(last_report_ts + self.report_cooldown)}:R>)", ephemeral=True)
        self.last_reports[user.id] = int(time.time())

        no_ban = set(roles).intersection([role.id for role in user.roles])

        if inter.author.id == user.id:
            return await inter.response.send_message("Nemůžeš nahlásit sám sebe.", ephemeral=True)
        if user.bot:
            return await inter.response.send_message("Nemůžeš nahlásit bota.", ephemeral=True)
        if no_ban:
            return await inter.response.send_message("Tohoto uživatele nemůžeš nahlásit.", ephemeral=True)

        timestamp = time.time() + 7890000  # plus 3 měsíce
        reports_from_db = db.child('reports').child(user.id).child('count').get().val() or 0
        db.child('reports').child(user.id).update({'count': reports_from_db + 1, 'time': timestamp})

        color = 0xeaa500 if reports_from_db == 0 else 0xea4700

        view = disnake.ui.View()
        view.add_item(disnake.ui.Button(label=str(user), url=f"discord://-/users/{user.id}"))
        view.add_item(disnake.ui.Button(label=str(inter.author), url=f"discord://-/users/{inter.author.id}"))

        if (reports_from_db + 1) >= 3:
            await user.ban()

            embed = disnake.Embed(title=f"{user.name}", color=0xea0017, timestamp=datetime.fromtimestamp(timestamp))
            embed.add_field(name="Ban: ", value="Ano", inline=True)
            embed.add_field(name="Důvod: ", value=f"Překročen maximální počet varování.", inline=True)
            embed.set_footer(text="Vyprší")

            await inter.response.send_message(f"Úspěšně zabanován uživatel **{user.name}**, počet varování **{reports_from_db + 1}**.")
            return await self.client.get_channel(warn_ch).send(embed=embed, view=view)

        embed = disnake.Embed(title=f"{user.name}", color=color, timestamp=datetime.fromtimestamp(timestamp))
        embed.add_field(name="Počet varování: ", value=f"{reports_from_db + 1}", inline=True)
        embed.add_field(name="Důvod: ", value=f"{reason}", inline=True)
        embed.add_field(name="Nahlásil: ", value=inter.author.name, inline=True)
        embed.set_footer(text="Vyprší")

        await inter.response.send_message(f"Úspěšně nahlášeno uživatele **{user.name}**, počet varování **{reports_from_db + 1}**.")
        return await self.client.get_channel(warn_ch).send(embed=embed, view=view)

    @commands.has_any_role(*roles)
    @commands.message_command(name="Report user")
    async def _report_app(
            self,
            inter: disnake.ApplicationCommandInteraction
    ):
        user = inter.target.author

        last_report_ts = self.last_reports.get(user.id, (time.time() - self.report_cooldown))
        if (time.time() - last_report_ts) < self.report_cooldown:
            return await inter.response.send_message(f"Ještě neuběhlo {int(self.report_cooldown/60)} minut od posledního reportu! (<t:{int(last_report_ts + self.report_cooldown)}:R>)", ephemeral=True)
        self.last_reports[user.id] = int(time.time())

        no_ban = set(roles).intersection([role.id for role in user.roles])

        if inter.author.id == user.id:
            return await inter.response.send_message("Nemůžeš nahlásit sám sebe.", ephemeral=True)
        if user.bot:
            return await inter.response.send_message("Nemůžeš nahlásit bota.", ephemeral=True)
        if no_ban:
            return await inter.response.send_message("Tohoto uživatele nemůžeš nahlásit.", ephemeral=True)

        timestamp = time.time() + 7890000  # plus 3 měsíce
        reports_from_db = db.child('reports').child(user.id).child('count').get().val() or 0
        db.child('reports').child(user.id).update({'count': reports_from_db + 1, 'time': timestamp})

        color = 0xeaa500 if reports_from_db == 0 else 0xea4700

        view = disnake.ui.View()
        view.add_item(disnake.ui.Button(label=str(user), url=f"discord://-/users/{user.id}"))
        view.add_item(disnake.ui.Button(label=str(inter.author), url=f"discord://-/users/{inter.author.id}"))

        if (reports_from_db + 1) >= 3:
            await user.ban()

            embed = disnake.Embed(title=f"{user.name}", color=0xea0017, timestamp=datetime.fromtimestamp(timestamp))
            embed.add_field(name="Ban: ", value="Ano", inline=True)
            embed.add_field(name="Důvod: ", value=f"Překročen maximální počet varování.", inline=True)
            embed.set_footer(text="Vyprší")

            await inter.response.send_message(f"Úspěšně zabanován uživatel **{user.name}**, počet varování **{reports_from_db + 1}**.")
            return await self.client.get_channel(warn_ch).send(embed=embed, view=view)

        embed = disnake.Embed(title=f"{user.name}", color=color, timestamp=datetime.fromtimestamp(timestamp))
        embed.add_field(name="Počet varování: ", value=f"{reports_from_db + 1}", inline=True)
        embed.add_field(name="Důvod: ", value=f"Automatický report", inline=True)
        embed.add_field(name="Nahlásil: ", value=inter.author.name, inline=True)
        embed.set_footer(text="Vyprší")

        await inter.response.send_message(f"Úspěšně nahlášen uživatel **{user.name}**, počet varování **{reports_from_db + 1}**.")
        return await self.client.get_channel(warn_ch).send(content=f"**Text zprávy:**\n`{inter.target.content}`", embed=embed, view=view)


def setup(client):
    client.add_cog(ReportCog(client))
