import disnake
from disnake.ext import commands
from disnake.ext.commands import Param

from pysychonaut import PsychonautWiki
pwiki = PsychonautWiki()


async def autocomplete_drugs(inter, string: str) -> list[str]:
    return [drug for drug in pwiki.substance_list if string.lower() in drug.lower()][:24]


def convert_drug_to_embed(drug: dict) -> disnake.Embed:
    drug = drug[0]

    name = drug["name"]
    roas = drug["roas"][0]

    embed = disnake.Embed(title=name, color=disnake.Color.random())

    dosage = roas["dose"]
    dose_units = dosage["units"]

    embed.add_field(name="\u200B", value="**Dosages**", inline=False)
    embed.add_field(name="Threshold", value=f"{dosage['threshold']} {dose_units}")

    return embed


class Drugs(commands.Cog):
    def __init__(self, client):
        """Example dickstring."""
        self.client = client

    @commands.slash_command(name="drug", description="Shows info about a given drug")
    async def _search_psychonaut_wiki(
            self,
            inter: disnake.ApplicationCommandInteraction,
            search: str = Param(autocomplete=autocomplete_drugs)
    ):
        result = pwiki.search_psychonaut_wiki(search)["substances"]
        if result:
            return await inter.send(embed=convert_drug_to_embed(result))
        return await inter.send("***You fucked up the name, or there is no record of this substance in our sources' database..***", ephemeral=True)


def setup(client):
    client.add_cog(Drugs(client))
