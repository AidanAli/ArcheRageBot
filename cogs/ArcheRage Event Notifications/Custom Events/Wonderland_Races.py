import pytz
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.combining import AndTrigger

from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from discord import Embed

from main import event_Ping


class WonderLand_races(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.scheduler = AsyncIOScheduler(timezone=pytz.timezone('US/Eastern'))
        self.scheduler.start()
        Merchants_Day = AndTrigger(
            [CronTrigger(hour=13, minute=44, day_of_week='sun', timezone=pytz.timezone('US/Eastern'))])
        self.scheduler.add_job(self.send_message, Merchants_Day)

    async def send_message(self):
        channel = self.client.get_channel(event_Ping)  # replace with your channel ID
        embed = Embed(title="Wonderland Races", description="Starts in`15`Minutes!",
                      color=0x00FF00)
        embed.set_image(url="https://i.ibb.co/X3qfnMh/Wonderland-Races-Banner.png")
        embed.set_thumbnail(
            url="https://1000logos.net/wp-content/uploads/2020/09/ArcheAge-logo.png")
        embed.add_field(
            name="Event Details",
            value="https://na.archerage.to/forums/threads/game-event-wonderland-races.11055/")

        self.client.loop.create_task(channel.send(embed=embed))

    @commands.Cog.listener()
    async def on_ready(self):
        print("Wonderland_Race Loaded")
        self.scheduler.start()


async def setup(client):
    await client.add_cog(WonderLand_races(client))
