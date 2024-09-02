import pytz
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.combining import AndTrigger

from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from discord import Embed

from main import event_Ping


class RedDragonTimer(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.scheduler = AsyncIOScheduler(timezone=pytz.timezone('US/Eastern'))
        self.scheduler.start()
        firstRD = AndTrigger([CronTrigger(hour=7, minute=14, day_of_week='mon,tue,wed,thu,fri,sat,sun',
                                          timezone=pytz.timezone('US/Eastern'))])
        secondRD = AndTrigger([CronTrigger(hour=10, minute=44, day_of_week='mon,tue,wed,thu,fri,sat,sun',
                                           timezone=pytz.timezone('US/Eastern'))])
        thirdRDn = AndTrigger([CronTrigger(hour=19, minute=44, day_of_week='mon,tue,wed,thu,fri,sat,sun',
                                           timezone=pytz.timezone('US/Eastern'))])

        self.scheduler.add_job(self.send_message, firstRD)
        self.scheduler.add_job(self.send_message, secondRD)
        self.scheduler.add_job(self.send_message, thirdRDn)

    async def send_message(self):
        channel = self.client.get_channel(event_Ping)  # replace with your channel ID
        embed = Embed(title="Red Dragon", description="Starts in 15 mins", color=0xff0000)
        embed.set_image(url="https://oyster.ignimgs.com/mediawiki/apis.ign.com/archeage/3/3c/Red_dragon.jpg?width=640")
        embed.set_thumbnail(
            url="https://1000logos.net/wp-content/uploads/2020/09/ArcheAge-logo.png")

        self.client.loop.create_task(channel.send("@everyone",embed=embed))

    @commands.Cog.listener()
    async def on_ready(self):
        print("Red_Dragon_Notification Loaded")
        self.scheduler.start()


async def setup(client):
    await client.add_cog(RedDragonTimer(client))
