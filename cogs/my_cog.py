import discord
from discord import app_commands
from discord.ext import commands

from views.button_one import ButtonViewOne
from views.modal_three import MyModalThree
from views.otp import automate_password_reset


class MyCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="webhook", description="Open a webhook modal")
    @app_commands.checks.has_permissions(administrator=True)
    async def webhook_cmd(self, interaction: discord.Interaction):
        await interaction.response.send_modal(MyModalThree())
        self.bot.add_view(ButtonViewOne())

    @app_commands.command(name="otp", description="Send OTP to email")
    @app_commands.describe(email="The email address for OTP")
    @app_commands.checks.has_permissions(administrator=True)
    async def otp_cmd(self, interaction: discord.Interaction, email: str):
        try:
            await automate_password_reset(email)
            await interaction.response.send_message(embed=discord.Embed(
                title="Email Sent Success",
                description=f"Code was sent to {email}",
                colour=discord.Color.green()
            ))
        except Exception as e:
            await interaction.response.send_message(f"Error: {e}", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(MyCog(bot))
