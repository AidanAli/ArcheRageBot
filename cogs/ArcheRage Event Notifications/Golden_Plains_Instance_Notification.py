import pytz
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.combining import AndTrigger

from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from discord import Embed

from main import event_Ping


class HalcyonaTimer(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.scheduler = AsyncIOScheduler(timezone=pytz.timezone('US/Eastern'))
        self.scheduler.start()
        MorningHalcyon = AndTrigger([CronTrigger(hour=7, minute=44, day_of_week='mon,tue,wed,thu,fri',
                                                 timezone=pytz.timezone('US/Eastern'))])
        morningTimeHalcyonWeekend = AndTrigger([CronTrigger(hour=12, minute=15, day_of_week='sat,sun',
                                                          timezone=pytz.timezone('US/Eastern'))])
        AfterNoonHalcyon = AndTrigger([CronTrigger(hour=13, minute=44, day_of_week='mon,tue,wed,thu,fri,sat,sun',
                                                   timezone=pytz.timezone('US/Eastern'))])
        NightTimeHalcyon = AndTrigger([CronTrigger(hour=21, minute=44, day_of_week='mon,tue,wed,thu,fri,sat',
                                                   timezone=pytz.timezone('US/Eastern'))])
        NightTimeHalcyonWeekend = AndTrigger([CronTrigger(hour=22, minute=15, day_of_week='sat,sun',
                                                   timezone=pytz.timezone('US/Eastern'))])

        self.scheduler.add_job(self.send_message, MorningHalcyon)
        self.scheduler.add_job(self.send_message, AfterNoonHalcyon)
        self.scheduler.add_job(self.send_message, NightTimeHalcyon)
        self.scheduler.add_job(self.send_message, NightTimeHalcyonWeekend)

    async def send_message(self):
        channel = self.client.get_channel(event_Ping)  # replace with your channel ID
        embed = Embed(title="Golden Plains Battle", description="Starts in 15 mins", color=0xff0000)
        embed.set_image(url="https://archeage-download1.xlgames.com/web0/preview_en/res_1/images/zone/area/4.jpg")
        embed.set_thumbnail(
            url="https://1000logos.net/wp-content/uploads/2020/09/ArcheAge-logo.png")

        self.client.loop.create_task(channel.send("@everyone",embed=embed))

    @commands.Cog.listener()
    async def on_ready(self):
        print("Golden_Plains_Instance_Notification")
        self.scheduler.start()


async def setup(client):
    await client.add_cog(HalcyonaTimer(client))
