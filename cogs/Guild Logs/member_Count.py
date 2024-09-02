import discord
from discord.ext import commands

class MemberCountChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def create_member_channel(self, ctx):
        """Creates a locked voice channel that tracks the number of members."""
        guild = ctx.guild

        # Check if a channel already exists with the same name format
        existing_channel = discord.utils.get(guild.channels, name__startswith="Members: ", type=discord.ChannelType.voice)
        if existing_channel:
            await ctx.send("A member count channel already exists.")
            return

        # Create a locked voice channel
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(connect=False),  # Locked for @everyone
            guild.me: discord.PermissionOverwrite(connect=True),  # Bot can connect
        }

        # Create the channel with the initial member count
        member_count = guild.member_count
        channel = await guild.create_voice_channel(f"Members: {member_count}", overwrites=overwrites)

        await ctx.send(f"Locked member count voice channel created: {channel.mention}")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Updates the channel name when a new member joins."""
        await self.update_member_count_channel(member.guild, change=1)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """Updates the channel name when a member leaves."""
        await self.update_member_count_channel(member.guild, change=-1)

    async def update_member_count_channel(self, guild, change):
        """Updates the member count in the relevant voice channel."""
        # Find the channel that tracks the member count
        channel = discord.utils.get(guild.channels, name__startswith="Members: ", type=discord.ChannelType.voice)

        if channel:
            # Extract the current count from the channel name
            current_count_str = channel.name.split(": ")[-1]
            try:
                current_count = int(current_count_str)
            except ValueError:
                current_count = guild.member_count

            # Update the count based on the change
            new_count = current_count + change
            new_name = f"Members: {new_count}"
            await channel.edit(name=new_name)

async def setup(bot):
    await bot.add_cog(MemberCountChannel(bot))
