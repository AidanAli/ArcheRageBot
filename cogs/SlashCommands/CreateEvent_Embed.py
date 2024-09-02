import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime, timedelta
import pytz


class Create_Event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='eventcreate', description='Create a raid event and allow users to apply.')
    async def eventcreate(
            self,
            interaction: discord.Interaction,
            title: str,
            description: str,
            attachment: discord.Attachment,
            event_time: int  # Accepts the event time in epoch numbers
    ):
        # Check if the user has the 'Event Manager' role
        required_role_name = "Events Manager"
        guild = interaction.guild
        member = guild.get_member(interaction.user.id)
        if discord.utils.get(member.roles, name=required_role_name) is None:
            await interaction.response.send_message("You don't have permission to create events.",
                                                     ephemeral=True)
            return

        eastern = pytz.timezone('US/Eastern')
        now = datetime.now(eastern)
        event_datetime = datetime.utcfromtimestamp(event_time)
        time_until_event = max(event_time - int(now.timestamp()), 0)
        hours, remainder = divmod(time_until_event, 3600)
        minutes, _ = divmod(remainder, 60)
        formatted_time = now.strftime('%Y-%m-%d %I:%M %p')
        formatted_event_time = f"<t:{event_time}>"

        event_embed = discord.Embed(
            title=title,  # Set event title
            description=description,  # Set event description
            color=0x00ff00
        )
        event_embed.set_image(url=attachment.url)  # Set attachment as thumbnail
        applied_users = []

        async def apply_button_callback(button_interaction: discord.Interaction):
            if button_interaction.user.id not in applied_users:
                applied_users.append(button_interaction.user.id)
                formatted_applicants = '\n'.join([f"<@{user_id}>" for user_id in applied_users])
                for field in event_embed.fields:
                    if field.name == "Applicants":
                        # Update the existing Applicants field
                        event_embed.set_field_at(event_embed.fields.index(field), name="Applicants",
                                                 value=f"{formatted_applicants}", inline=False)
                        break
                else:
                    # Add a new Applicants field if it doesn't exist
                    event_embed.add_field(name="Applicants", value=f"{formatted_applicants}", inline=False)
                await button_interaction.message.edit(embed=event_embed, view=view)
                await button_interaction.response.send_message("You have successfully applied for the event.",
                                                               ephemeral=True)
            else:
                await button_interaction.response.send_message("You have already applied for this event.",
                                                               ephemeral=True)

        async def opt_out_button_callback(button_interaction: discord.Interaction):
            if button_interaction.user.id in applied_users:
                applied_users.remove(button_interaction.user.id)
                formatted_applicants = '\n'.join([f"<@{user_id}>" for user_id in applied_users])
                for field in event_embed.fields:
                    if field.name == "Applicants":
                        event_embed.set_field_at(event_embed.fields.index(field), name="Applicants",
                                                 value=f"{formatted_applicants}", inline=False)
                        break
                await button_interaction.message.edit(embed=event_embed, view=view)
                await button_interaction.response.send_message("You have opted out of the event.", ephemeral=True)
            else:
                await button_interaction.response.send_message("You have not applied for this event.", ephemeral=True)

        async def end_event_button_callback(button_interaction: discord.Interaction):
            member = button_interaction.user
            guild = button_interaction.guild
            required_role_name = "Events Manager"

            # Check if the member has the required role
            required_role = discord.utils.get(guild.roles, name=required_role_name)
            if required_role in member.roles:
                await button_interaction.message.delete()
                await button_interaction.response.send_message("Event ended successfully.", ephemeral=True)
            else:
                await button_interaction.response.send_message("You don't have permission to end this event.",
                                                               ephemeral=True)

        view = discord.ui.View()
        apply_button = discord.ui.Button(label="Apply For Event", style=discord.ButtonStyle.green)
        apply_button.callback = apply_button_callback
        view.add_item(apply_button)

        opt_out_button = discord.ui.Button(label="Opt Out", style=discord.ButtonStyle.red)
        opt_out_button.callback = opt_out_button_callback
        view.add_item(opt_out_button)

        end_event_button = discord.ui.Button(label="End Event", style=discord.ButtonStyle.red)
        end_event_button.callback = end_event_button_callback  # Correctly attaching the callback function
        view.add_item(end_event_button)

        event_embed.add_field(name="Event Start Time", value=formatted_event_time,
                              inline=False)  # Display event time in Discord timestamp format

        event_embed.set_footer(text=f"Event Created by {interaction.user.display_name} • {formatted_time}")

        message = await interaction.response.send_message(embed=event_embed, view=view)


async def setup(bot):
    await bot.add_cog(Create_Event(bot), guilds=[discord.Object(id="1271649288791003217")])
