from disnake.ext import commands


class AppErrors(commands.Cog):
    def __init__(self, client):
        """Errors."""
        self.client = client

    @commands.Cog.listener()
    async def on_message_command_error(self, inter, error):
        # All errors under "CheckFailure" (https://disnake.readthedocs.io/en/latest/ext/commands/api.html#exception-hierarchy)
        match error:
            case commands.CheckAnyFailure:
                message = "Pravěpodobně nemá dostatečná práva k provedení akce."
            case commands.PrivateMessageOnly:
                message = "Tento příkaz lze použít pouze v soukromé zprávě."
            case commands.NoPrivateMessage:
                message = "Tento příkaz nelze použít pouze v soukromé zprávě."
            case commands.NotOwner:
                message = "Musíš být big PP dev, abys na tohle měl práva."
            case commands.MissingPermissions:
                message = "Na tohle nemáš práva."
            case commands.BotMissingPermissions:
                message = "K provedení této akce mi chybí práva."
            case commands.MissingRole:
                message = "Na tohle nemáš dostatečné práva."
            case commands.BotMissingRole:
                message = "K provedení této akce mi chybí role."
            case commands.MissingAnyRole:
                message = "Na tohle nemáš dostatečnou roli."
            case commands.BotMissingAnyRole:
                message = "K provedení této akce mi chybí role."
            case commands.NSFWChannelRequired:
                message = "Tento příkaz lze používat jen v NSFW místnotech."
            case _:
                message = "Neočekávaná chyba. Pokud problém přetrvává informuj vývojáře."

        if inter.response.is_done():
            return await inter.edit_original_message(content=message)

        await inter.response.send_message(message, ephemeral=True)


def setup(client):
    client.add_cog(AppErrors(client))
