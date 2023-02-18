from discord.ext import commands
from discord.ext.commands import Cog

from pathlib import Path
from time import time


class Bot(commands.Bot):
    def __init__(self, command_prefix=..., help_command=..., **options):
        super().__init__(command_prefix, help_command, **options)
        self.load_extensions()
        self.uptime = round(time())

    @Cog.listener()
    async def on_ready(self) -> None:
        print(f"{self.user} ready!")

    def load_extensions(self, names: list = None) -> None:
        """Load extensions from the bot

        Parameters
        -----------
        names: :class: 'list'
            The list of names of extensions that need to be loaded, None = all.

        Returns
        --------
        errors: :class: 'dict'
            The exception occured in extensions.
        """

        path = Path("bot/exts/")
        errors = {}
        for extension in path.glob("**/*.py"):
            extension = str(extension).replace("/", ".")[:-3]
            if names and extension not in names:
                continue
            try:
                self.load_extension(extension, store=False)
            except Exception as e:
                errors[extension] = e
        print(errors)
        return errors

    def reload_extensions(self, names: list = None) -> None:
        """Reload extensions from the bot

        Parameters
        -----------
        names: :class: 'list'
            The list of names of extensions that need to be loaded, None = all.

        Returns
        --------
        errors: :class: 'dict'
            The exception occured in extensions.
        """

        path = Path("bot/exts/")
        errors = {}
        for extension in path.glob("**/*.py"):
            extension = str(extension).replace("/", ".")[:-3]
            if names and extension not in names:
                continue
            try:
                self.reload_extension(extension)
            except Exception as e:
                errors[extension] = e
        print(errors)
        return errors

    def unload_extensions(self, names: list = None) -> None:
        """Unload extensions from the bot

        Parameters
        -----------
        names: :class: 'list'
            The list of names of extensions that need to be loaded, None = all.

        Returns
        --------
        errors: :class: 'dict'
            The exception occured in extensions.
        """

        path = Path("bot/exts/")
        errors = {}
        for extension in path.glob("**/*.py"):
            extension = str(extension).replace("/", ".")[:-3]
            if names and extension not in names:
                continue
            try:
                self.unload_extension(extension)
            except Exception as e:
                errors[extension] = e
        print(errors)
        return errors
