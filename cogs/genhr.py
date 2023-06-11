import disnake
from disnake.ext import commands
import yaml

config = yaml.safe_load(open("config.yml"))
roles = config.get("report_roles")


class GenHr(commands.Cog):
    """genhr command"""

    def __init__(self, client):
        self.client = client
        self.last_reports = {}

    @commands.has_any_role(*roles)
    @commands.slash_command(name="genhr", description="Report command")
    async def _report(
            self,
            inter: disnake.ApplicationCommandInteraction,
    ):
        color = 0xff3d3d

        index = 1
        rules = [
            "!Vždy si buďte jistí tím, co berete - ani u internetových vendorů není 100% jistota, že máte vážně látku, kterou jste si objednali, u street dealerů je to ještě horší. Není nic lehčího, než si koupit testkity (např. ze stránky protestkit.eu), a každý batch nejdříve otestovat. Pokud na látku neexistuje testkit, a máte jakékoliv podezření, že se jedná o jinou substanci, radši se konzumaci vyhněte! V nejhorším případě ji alespoň dávkujte jako nejsilnější možnou alternativu, tedy od nejnižších dávek.",
            "!Substance si před konzumací zvažte - obvzlášť, pokud se jedná o vysoce potentní látky. Miligramová váha stojí pár stovek (CZK), což je malá cena za ochranu zdraví, eyeballing (dávkování od oka) může být velice nebezpečný. Vždy začínejte na nízké dávce, vždy můžete přidat, ale nikdy nemůžete ubrat, a to, co někteří lidé zvládají v pohodě, vám může např. kvůli vaší citlivosti ublížit.",
            "!Nikdy neužívejte látky sami a bez toho, aniž by o tom někdo věděl - vždy by o tom někdo měl vědět, v případě, že by nastaly jakékoliv komplikace.",
            "Nikdy se nenechte do konzumace látek nutit - pokud nechcete, rázně odmítněte. A s nikým se v užívání nepředhánějte. Drogy nejsou sport.",
            "!Před užitím si udělejte o látkách náležitý research - např. Psychonautwiki je skvělý zdroj informací, ale mějte na vědomí, že i tam se mohou vyskytovat chyby! Především by vás mělo zajímat dávkování (pozor na rozlišení dávkování u různých způsobů užití, například dávkování při kouření a orální konzumaci se velmi liší), doba trvání účinků, nebezpečné interakce s jinými látkami, očekávatelné efekty a bezpečnostní profil.",
            "Vyhněte se užívání, pokud jste v psychické nepohodě - mějte na paměti, že drogy nejsou řešení jakýchkoliv problémů, a určité látky mohou některé psychické komplikace výrazně zhoršit. Užívání látek za účelem potlačení problémů nebo užívání několik dní po sobě zpravidla vede k závislosti a zhoršení stavu.",
            "!Pokud vidíte, že má někdo problém, neváhejte v akutních případech ihned pomoct, v těch méně akutních alespoň pomoc nabídnout. Můžete tím někomu zachránit život!",
            "Pokud užíváte substance šňupáním, vyvarujte se používání bankovek - nejen, že na nich zůstávaji stopové množství substancí, ale je to zároveň extrémně nehygienické. Stejně tak byste své šňupátko neměli sdílet s ostatními lidmi z důvodu minimalizace rizik přenosu chorob."
        ]

        embed = disnake.Embed(title="Všeobecná pravidla Harm Reduction", color=color)

        for rule in rules:
            emote = "<a:ano:974371973775888425>" if rule.startswith("!") else "<a:ne:974371979874410507>"

            embed.add_field(name=f"\u200B\n{emote}", value=f"**{index} »** {rule.replace('!', '')}" + "", inline=False)
            index += 1

        await inter.channel.send(embed=embed)


def setup(client):
    client.add_cog(GenHr(client))
