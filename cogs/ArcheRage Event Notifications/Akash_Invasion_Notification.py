import pytz
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.combining import AndTrigger

from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from discord import Embed

from main import event_Ping


class AkashInvasion(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.scheduler = AsyncIOScheduler(timezone=pytz.timezone('US/Eastern'))
        self.scheduler.start()
        akashInvasionMorning = AndTrigger([CronTrigger(hour=8, minute=14, day_of_week='mon,wed,sat', timezone=pytz.timezone('US/Eastern'))])
        akashInvasionEvening = AndTrigger([CronTrigger(hour=16, minute=14, day_of_week='mon,wed,sat', timezone=pytz.timezone('US/Eastern'))])
        akashInvasionNight = AndTrigger([CronTrigger(hour=21, minute=14, day_of_week='mon,wed,sat', timezone=pytz.timezone('US/Eastern'))])

        self.scheduler.add_job(self.send_message, akashInvasionMorning)
        self.scheduler.add_job(self.send_message, akashInvasionEvening)
        self.scheduler.add_job(self.send_message, akashInvasionNight)

    async def send_message(self):
        channel = self.client.get_channel(event_Ping)  # replace with your channel ID
        embed = Embed(title="Akasch Invasion", description="in 15 Minutes", color=0xff0000)
        embed.set_image(url="https://movieview.dk/wp-content/uploads/2021/03/ScreenShot1470.jpg")
        embed.set_thumbnail(
            url="https://1000logos.net/wp-content/uploads/2020/09/ArcheAge-logo.png")

        self.client.loop.create_task(channel.send("@everyone",embed=embed))

    @commands.Cog.listener()
    async def on_ready(self):
        print("Akash_Invasion_Notification Loaded")
        self.scheduler.start()


async def setup(client):
    await client.add_cog(AkashInvasion(client))