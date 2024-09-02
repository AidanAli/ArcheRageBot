import pytz
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.combining import AndTrigger

from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from discord import Embed

from main import event_Ping


class WeeklyReset(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.scheduler = AsyncIOScheduler(timezone=pytz.timezone('US/Eastern'))
        self.scheduler.start()
        weeklyReset = AndTrigger([CronTrigger(hour=23, minute=30, day_of_week='sun', timezone=pytz.timezone('US/Eastern'))])

        self.scheduler.add_job(self.send_message, weeklyReset)

    async def send_message(self):
        channel = self.client.get_channel(event_Ping)  # replace with your channel ID
        embed = Embed(title="Weekly Reset", description="Spawns in 30 Minutes", color=0xff0000)
        embed.set_thumbnail(
            url="https://1000logos.net/wp-content/uploads/2020/09/ArcheAge-logo.png")

        self.client.loop.create_task(channel.send("@everyone",embed=embed))

    @commands.Cog.listener()
    async def on_ready(self):
        print("Weekly_Reset_Notification Loaded")
        self.scheduler.start()


async def setup(client):
    await client.add_cog(WeeklyReset(client))
