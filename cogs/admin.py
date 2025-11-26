import discord
from discord import app_commands
from discord.ext import commands


class Admin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        # Define a command group
        self.sync_group = app_commands.Group(name="sync", description="Sync bot commands")
        self.bot.tree.add_command(self.sync_group)

        # Add subcommands to the group
        self.sync_group.add_command(
            app_commands.Command(
                name="global",
                description="Sync global commands",
                callback=self.sync_global
            )
        )

        self.sync_group.add_command(
            app_commands.Command(
                name="duplicate",
                description="Clear duplicates",
                callback=self.sync_clear_duplicates
            )
        )

    async def sync_global(self, interaction: discord.Interaction):
        if interaction.user.id not in self.bot.admins:
            await interaction.response.send_message("Not allowed.", ephemeral=True)
            return
        synced = await self.bot.tree.sync(guild=None)
        await interaction.response.send_message(f"Successfully synced {len(synced)} commands.")

    async def sync_clear_duplicates(self, interaction: discord.Interaction):
        if interaction.user.id not in self.bot.admins:
            await interaction.response.send_message("Not allowed.", ephemeral=True)
            return
        for guild in self.bot.guilds:
            self.bot.tree.clear_commands(guild=guild)
            await self.bot.tree.sync(guild=guild)
        await interaction.response.send_message("Successfully cleared duplicates.")


async def setup(bot: commands.Bot):
    await bot.add_cog(Admin(bot))
