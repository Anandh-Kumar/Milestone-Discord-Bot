from discord import ApplicationContext, Color, Embed
from discord.ext.commands import Cog, slash_command, is_owner
from dotenv import load_dotenv
from subprocess import run
from json import dump, load
from os import getenv

from bot.bot import Bot
from bot.constants import EMOJI

load_dotenv()


class Update(Cog):
    def __init__(self, bot: Bot) -> None:
        super().__init__()
        self.bot = bot

    def install_libraries(self):
        """Install all libraries used by bot using requirements.txt"""

        output = run(["pip", "install", "-r", "requirements.txt"], capture_output=True)

        return output

    def pull_code(self):
        """Pull latest code from github."""

        output = run(["git", "pull"], capture_output=True)

        return output

    def revert_code(self):
        with open(getenv("JSON_PATH"), "r", encoding="UTF-8") as json_file:
            CONSTANTS = load(json_file)
        safe_state = CONSTANTS.get("BOTS_CONSTANTS", {}).get("SAFE_STATE", None)

        if safe_state == None:
            return

        output = run(["git", "reset", --"hard", safe_state])

        return output

    def save_state(self):
        output = run(["git", "log", "--oneline"], capture_output=True)

        if output.returncode == 0:
            commit_id = output.stdout.decode("utf-8").split(" ")[0]

            # Save it in json file
            with open(getenv("JSON_PATH"), "r", encoding="UTF-8") as json_file:
                CONSTANTS = load(json_file)

            CONSTANTS["BOT_CONSTANTS"]["SAFE_STATE"] = commit_id

            with open(getenv("JSON_PATH"), "w", encoding="UTF-8") as json_file:
                dump(CONSTANTS, json_file)

        return output

    async def send_output(self, ctx: ApplicationContext, output) -> None:
        if output.returncode == 0:
            message = output.stdout.decode("utf-8").replace("\n", "\n\n")
        else:
            message = output.stderr.decode("utf-8").replace("\n", "\n\n")

        embed = Embed(description=message, color=Color.from_rgb(47, 49, 54))
        await ctx.channel.send(embed=embed)

    @slash_command(
        name="update", description="Updates the bot with latest version of code."
    )
    @is_owner()
    async def _command(self, ctx: ApplicationContext) -> None:
        embed = Embed(
            description=f"Bot is going to update {EMOJI.UPDATING}.",
            color=Color.from_rgb(47, 49, 54),
        )

        await ctx.respond(embed=embed)

        await self.send_output(ctx, self.pull_code())
        await self.send_output(ctx, self.install_libraries())

        self.bot.unload_extensions()
        errors = self.bot.load_extensions()

        if len(errors) > 0:
            message = "Updating bot failed. Reverting back.\n\n"
            for error in errors:
                message = message + str(error) + "\n\n"

            embed.description = message
            await ctx.channel.send(embed=embed)

            await self.send_output(ctx, self.revert_code())
        else:
            embed.description = "Bot updated successfully. Saving current state."
            await ctx.channel.send(embed=embed)
            await self.send_output(ctx, self.save_state())


def setup(bot: Bot) -> None:
    bot.add_cog(Update(bot))
