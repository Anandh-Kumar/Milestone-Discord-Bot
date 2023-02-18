from discord import ApplicationContext, Color, Embed
from discord.ext.commands import Cog, slash_command, is_owner

from bot.bot import Bot


class Shutdown(Cog):
    def __init__(self, bot: Bot) -> None:
        super().__init__()
        self.bot = bot

    @slash_command(name="shutdown", description="Shutdown the bot.")
    @is_owner()
    async def _command(self, ctx: ApplicationContext) -> None:
        # Sends a reply embed
        embed = Embed(
            description=f"Bot is shutting down :apple:!",
            color=Color.from_rgb(47, 49, 54),
        )
        await ctx.respond(embed=embed)

        await self.bot.close()


def setup(bot: Bot) -> None:
    bot.add_cog(Shutdown(bot))
