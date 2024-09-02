import pytz
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.combining import AndTrigger

from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from discord import Embed

from main import event_Ping


class KrakenTimer(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.scheduler = AsyncIOScheduler(timezone=pytz.timezone('US/Eastern'))
        self.scheduler.start()
        Tue_SatKraken = AndTrigger([CronTrigger(hour=18, minute=14, day_of_week='tue,sat', timezone=pytz.timezone('US/Eastern'))])
        Sunday_kraken = AndTrigger([CronTrigger(hour=10, minute=14, day_of_week='sun', timezone=pytz.timezone('US/Eastern'))])
        self.scheduler.add_job(self.send_message, Tue_SatKraken)
        self.scheduler.add_job(self.send_message, Sunday_kraken)

    async def send_message(self):
        channel = self.client.get_channel(event_Ping)  # replace with your channel ID
        embed = Embed(title="Kraken World Boss Arcadian Sea", description="Spawns in 15 Minutes", color=0xff0000)
        embed.set_image(url="https://mmos.com/wp-content/uploads/2022/07/archeage-abyssal-kraken-world-boss.jpg")
        embed.set_thumbnail(
            url="https://1000logos.net/wp-content/uploads/2020/09/ArcheAge-logo.png")

        self.client.loop.create_task(channel.send("@everyone",embed=embed))

    @commands.Cog.listener()
    async def on_ready(self):
        print("Kraken_Notification Loaded")
        self.scheduler.start()


async def setup(client):
    await client.add_cog(KrakenTimer(client))
