import disnake
from disnake.ext import commands
import yaml

config = yaml.safe_load(open("config.yml"))
roles = config.get("report_roles")


class GenRules(commands.Cog):
    """genrules command"""

    def __init__(self, client):
        self.client = client
        self.last_reports = {}

    @commands.has_any_role(*roles)
    @commands.slash_command(name="genrules", description="Report command")
    async def _report(
            self,
            inter: disnake.ApplicationCommandInteraction,
    ):
        color = 0xff3d3d

        index = 1
        rules = [
            "! Uživateli je zakázáno jakýmkoliv způsobem urážet, ponižovat či zesměšňovat jiné členy naší komunity - pamatujte na základy slušného chování a respekt k ostatním.",
            "! Je striktně zakázáno šíření toxikomanie v jakékoliv formě, tzn.podávání informací o tom, jak pěstovat, prodávat, kupovat, distribuovat a nebo vyrábět substance.Tohle pravidlo se vztahuje i na soukromé zprávy",
            "! Je zakázáno rozesílat jakýkoliv nevhodný obsah mimo NSFW místnosti, stejně tak je striktně zakázáno sířit osobní údaje ostatních členů.",
            "! Vstup na server je zakázán osobám mladším 15 let.",
            "! Vše, co se píše na serveru je nutné brát s nadsázkou, tudíž žádný obsah nelze použít jako důkazní materiál. Na serveru působí externí Harm Reduction profesionálové, kteří jsou zde přítomní pro snížení rizika užívání drog a šíření osvěty a neručí za jimi neprodukovaný obsah případně se vyskytující na tomto serveru",
            "! Je přísně zakázáno obcházet jakýkoliv trest, ať už pomocí více účtů, proxy či VPN. Pokud má člen jakýkoliv aktivní trest, musí si trest odpykat.",
            "V neposlední řadě se zamyslete nad tím, co píšete, i když to není zmíněné v pravidlech. Vaše nepřiměřené chování může mít negativní dopad na psychiku ostatních členů, včetně posílání rad, které jsou hlouposti, zlehčování některých situací apod.",
            "Jakožto moderátoři si vyhrazujeme právo takové zprávy mazat, případně upozornit na jejich nepravdivé podklady, potrestat vás a také vás ze serveru zabanovat.",
            "Berte v potaz, že ctíme zákony České a Slovenské republiky, ToS Discordu a tak se vám reakce může zdát nepřiměřená situaci."
        ]

        embed = disnake.Embed(title="Pravidla", color=color)

        for rule in rules:
            emote = "<a:ano:974371973775888425>" if rule.startswith("!") else "<a:ne:974371979874410507>"

            embed.add_field(name=f"\u200B\n{emote}", value=f"**{index} »** {rule.replace('!', '')}" + "", inline=False)
            index += 1

        await inter.channel.send(embed=embed)


def setup(client):
    client.add_cog(GenRules(client))
