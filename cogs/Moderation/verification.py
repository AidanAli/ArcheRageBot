import discord
from discord.ext import commands
from discord import app_commands

from main import Guild_ID


class YourCogName(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="verify", description="Verify your Discord Account")
    async def verification(self, interaction, game_name: str, guild_name: str, character_info: discord.Attachment):
        # Fetch the member who used the command
        member = interaction.user

        avatar_url = member.avatar.url if member.avatar else member.default_avatar.url
        embed = discord.Embed(title="✅ Verification Request",
                              description=f"{member.mention}",
                              color=discord.Color.blurple())
        embed.add_field(name="Guild:", value=f"`<{guild_name}>`", inline=True)
        embed.add_field(name="In-game Name:", value=f"`{game_name}`", inline=True)

        # Set the image URL from the attachment
        embed.set_image(url=character_info.url)
        embed.set_thumbnail(url=avatar_url)

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(YourCogName(bot), guilds=[discord.Object(id=Guild_ID)])