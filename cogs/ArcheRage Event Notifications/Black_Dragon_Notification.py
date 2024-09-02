import pytz
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.combining import AndTrigger

from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from discord import Embed

from main import event_Ping


class BlackDragonTimer(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.scheduler = AsyncIOScheduler(timezone=pytz.timezone('US/Eastern'))
        self.scheduler.start()
        tueNight = AndTrigger([CronTrigger(hour=19, minute=44, day_of_week='tue', timezone=pytz.timezone('US/Eastern'))])
        satAfternoon = AndTrigger([CronTrigger(hour=16, minute=44, day_of_week='sat', timezone=pytz.timezone('US/Eastern'))])
        sunMorning = AndTrigger([CronTrigger(hour=8, minute=44, day_of_week='sun', timezone=pytz.timezone('US/Eastern'))])

        self.scheduler.add_job(self.send_message, tueNight)
        self.scheduler.add_job(self.send_message, satAfternoon)
        self.scheduler.add_job(self.send_message, sunMorning)

    async def send_message(self):
        channel = self.client.get_channel(event_Ping)  # replace with your channel ID
        embed = Embed(title="Black Dragon", description="Starts in 15 mins", color=0xff0000)
        embed.set_image(url="https://cdn.uc.assets.prezly.com/526b1c74-914d-4515-995d-abb65dcd82ee/-/preview/1200x1200/-/format/auto/")
        embed.set_thumbnail(
            url="https://1000logos.net/wp-content/uploads/2020/09/ArcheAge-logo.png")

        self.client.loop.create_task(channel.send("@everyone",embed=embed))

    @commands.Cog.listener()
    async def on_ready(self):
        print("Black_Dragon_Notification Loaded")
        self.scheduler.start()


async def setup(client):
    await client.add_cog(BlackDragonTimer(client))
