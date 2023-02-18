from discord import ApplicationContext, Color, Embed
from discord.ext.commands import Cog, slash_command, is_owner
from datetime import timedelta
from psutil import cpu_percent, virtual_memory
from time import time

from bot.bot import Bot
from bot.constants import EMOJI


class Status(Cog):
    def __init__(self, bot: Bot) -> None:
        super().__init__()
        self.bot = bot

    @slash_command(name="status", description="Get status of bot.")
    async def _command(self, ctx: ApplicationContext) -> None:
        latency = round(self.bot.latency * 1000)
        ram_usage = round(virtual_memory()[3] / 1000000000, 2)
        uptime_seconds = round(time()) - self.bot.uptime
        uptime = str(timedelta(seconds=uptime_seconds))

        embed = Embed(
            color=Color.from_rgb(47, 49, 54),
        )
        embed.add_field(
            name=f"Bot's  Ping  {EMOJI.LATENCY}", value=f"{latency}ms", inline=False
        )
        embed.add_field(
            name=f"Cpu Usage  {EMOJI.CPU}", value=f"{cpu_percent()}%", inline=False
        )
        embed.add_field(
            name=f"Ram Usage {EMOJI.RAM}", value=f"{ram_usage}GB", inline=False
        )
        embed.add_field(name=f"Last  Down  {EMOJI.UPTIME}", value=uptime)

        await ctx.respond(embed=embed)


def setup(bot: Bot) -> None:
    bot.add_cog(Status(bot))
