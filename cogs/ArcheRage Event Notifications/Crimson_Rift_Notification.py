import pytz
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.combining import AndTrigger

from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from discord import Embed

from main import event_Ping


class CrimsonRift(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.scheduler = AsyncIOScheduler(timezone=pytz.timezone('US/Eastern'))
        self.scheduler.start()
        firstAmCR= AndTrigger([CronTrigger(hour=00, minute=4, day_of_week='mon,tue,wed,thu,fri,sat,sun', timezone=pytz.timezone('US/Eastern'))])
        secondAmCR = AndTrigger([CronTrigger(hour=4, minute=4, day_of_week='mon,tue,wed,thu,fri,sat,sun', timezone=pytz.timezone('US/Eastern'))])
        thirdAmCr = AndTrigger([CronTrigger(hour=8, minute=4, day_of_week='mon,tue,wed,thu,fri,sat,sun', timezone=pytz.timezone('US/Eastern'))])
        firstPmCr = AndTrigger([CronTrigger(hour=12, minute=4, day_of_week='mon,tue,wed,thu,fri,sat,sun',timezone=pytz.timezone('US/Eastern'))])
        secondPMCr = AndTrigger([CronTrigger(hour=16, minute=4, day_of_week='mon,tue,wed,thu,fri,sat,sun', timezone=pytz.timezone('US/Eastern'))])
        ThirdPMCr = AndTrigger([CronTrigger(hour=20, minute=4, day_of_week='mon,tue,wed,thu,fri,sat,sun',timezone=pytz.timezone('US/Eastern'))])

        self.scheduler.add_job(self.send_message, firstAmCR)
        self.scheduler.add_job(self.send_message, secondAmCR)
        self.scheduler.add_job(self.send_message, thirdAmCr)
        self.scheduler.add_job(self.send_message, firstPmCr)
        self.scheduler.add_job(self.send_message, secondPMCr)
        self.scheduler.add_job(self.send_message, ThirdPMCr)

    async def send_message(self):
        channel = self.client.get_channel(event_Ping)  # replace with your channel ID
        embed = Embed(title="Crimson Rift", description="**Spawns in 15 Minutes**", color=0xff0000)
        embed.set_image(url="https://archeage-download1.sea.archeage.com/web/What3.PNG")
        embed.set_thumbnail(
            url="https://1000logos.net/wp-content/uploads/2020/09/ArcheAge-logo.png")

        self.client.loop.create_task(channel.send("@everyone",embed=embed))

    @commands.Cog.listener()
    async def on_ready(self):
        print("Crimson_Rift_Notification Loaded")
        self.scheduler.start()


async def setup(client):
    await client.add_cog(CrimsonRift(client))
