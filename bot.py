import logging
import os
import sys

import discord
from discord.ext import commands

import config
from views.button_one import ButtonViewOne


class PhobosBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=None,  
            case_insensitive=True,
            intents=discord.Intents.all(),
            allowed_mentions=discord.AllowedMentions(roles=False, everyone=False, users=True),
            application_id=config.APPLICATION_ID  
        )
        self.logger = logging.getLogger("bot")
        self.admins = [1313648833766625361]

    async def setup_hook(self) -> None:
        await self.load_cogs()
        
        await self.tree.sync()
        self.logger.info("Slash command s synced globally.")

    async def on_ready(self):
        self.add_view(ButtonViewOne())
        self.logger.info(f"Logged in as {self.user} | ID: {self.user.id}")

    @staticmethod
    def setup_logging() -> None:
        logging.getLogger("discord").setLevel(logging.INFO)
        logging.getLogger("discord.http").setLevel(logging.WARNING)
        logging.basicConfig(
            level=logging.INFO,
            format="%(levelname)s | %(asctime)s | %(name)s | %(message)s",
            stream=sys.stdout,
        )

    async def load_cogs(self, directory="./cogs") -> None:
        for file in os.listdir(directory):
            path = os.path.join(directory, file)
            if file.endswith(".py") and not file.startswith("_"):
                ext = f"{directory[2:].replace('/', '.')}.{file[:-3]}"
                try:
                    await self.load_extension(ext)
                    self.logger.info(f"Loaded: {file[:-3]}")
                except Exception as e:
                    self.logger.error(f"Failed to load {file[:-3]}: {e}")
            elif os.path.isdir(path) and not file.startswith("_"):
                await self.load_cogs(path)

        
        try:
            await self.load_extension("jishaku")
        except Exception as e:
            self.logger.error(f"Failed to load jishaku: {e}")


if __name__ == "__main__":
    bot = PhobosBot()
    bot.setup_logging()
    bot.run(config.TOKEN, log_handler=None)
