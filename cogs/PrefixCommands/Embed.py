import discord
from discord.ext import commands
from discord import ui


class Embed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Utility Cog Loaded")

    @commands.command(name="p")
    async def progressbar(self, ctx, progress: int):
        # Calculate the progress bar
        bar_length = 10
        filled_length = int(round(bar_length * progress / 100))
        bar_fill = '<:ortabaryesil47:1237996787281952831>'
        bar_empty = '<a:whiteline:1238015761172267020> '

        # Construct the progress bar string
        progress_bar = ''.join([bar_fill if i < filled_length else bar_empty for i in range(bar_length)])

        # Create the embed
        embed = discord.Embed(title="Progress Bar", description=f"{progress_bar} {progress}%")
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Embed(bot))
