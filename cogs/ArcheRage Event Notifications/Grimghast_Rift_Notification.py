import pytz
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.combining import AndTrigger

from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from discord import Embed

from main import event_Ping


class GrimghastRift(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.scheduler = AsyncIOScheduler(timezone=pytz.timezone('US/Eastern'))
        self.scheduler.start()
        firstGr = AndTrigger([CronTrigger(hour=2, minute=5, day_of_week='mon,tue,wed,thu,fri,sat,sun', timezone=pytz.timezone('US/Eastern'))])
        secondGr = AndTrigger([CronTrigger(hour=6, minute=5, day_of_week='mon,tue,wed,thu,fri,sat,sun', timezone=pytz.timezone('US/Eastern'))])
        thirdGr = AndTrigger([CronTrigger(hour=10, minute=5, day_of_week='mon,tue,wed,thu,fri,sat,sun', timezone=pytz.timezone('US/Eastern'))])
        forthtGr = AndTrigger([CronTrigger(hour=14, minute=5, day_of_week='mon,tue,wed,thu,fri,sat,sun',timezone=pytz.timezone('US/Eastern'))])
        fifthGr = AndTrigger([CronTrigger(hour=18, minute=5, day_of_week='mon,tue,wed,thu,fri,sat,sun', timezone=pytz.timezone('US/Eastern'))])
        sixthGr = AndTrigger([CronTrigger(hour=22, minute=5, day_of_week='mon,tue,wed,thu,fri,sat,sun',timezone=pytz.timezone('US/Eastern'))])

        self.scheduler.add_job(self.send_message, firstGr)
        self.scheduler.add_job(self.send_message, secondGr)
        self.scheduler.add_job(self.send_message, thirdGr)
        self.scheduler.add_job(self.send_message, forthtGr)
        self.scheduler.add_job(self.send_message, fifthGr)
        self.scheduler.add_job(self.send_message, sixthGr)

    async def send_message(self):
        channel = self.client.get_channel(event_Ping)  # replace with your channel ID
        embed = Embed(title="Grimghast Rift", description="**Spawns in 15 Minutes**", color=0xff0000)
        embed.set_image(url="https://archeage-download1.sea.archeage.com/web/What3.PNG")
        embed.set_thumbnail(
            url="https://1000logos.net/wp-content/uploads/2020/09/ArcheAge-logo.png")

        self.client.loop.create_task(channel.send("@everyone",embed=embed))

    @commands.Cog.listener()
    async def on_ready(self):
        print("Grimghast_Rift_Notification")
        self.scheduler.start()


async def setup(client):
    await client.add_cog(GrimghastRift(client))
