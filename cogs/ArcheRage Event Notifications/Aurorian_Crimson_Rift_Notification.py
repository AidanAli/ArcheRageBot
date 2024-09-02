import pytz
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.combining import AndTrigger

from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from discord import Embed

from main import event_Ping


class AurorianCR(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.scheduler = AsyncIOScheduler(timezone=pytz.timezone('US/Eastern'))
        self.scheduler.start()
        first_AurorianCR_PM = AndTrigger([CronTrigger(hour=13, minute=4, day_of_week='mon,tue,wed,thu,fri,sat,sun', timezone=pytz.timezone('US/Eastern'))])
        second_AurorianCR_PM = AndTrigger([CronTrigger(hour=17, minute=4, day_of_week='mon,tue,wed,thu,fri,sat,sun', timezone=pytz.timezone('US/Eastern'))])
        third_AurorianCR_PM = AndTrigger([CronTrigger(hour=21, minute=4, day_of_week='mon,tue,wed,thu,fri,sat,sun', timezone=pytz.timezone('US/Eastern'))])
        firstAurorianCR_AM = AndTrigger([CronTrigger(hour=1, minute=4, day_of_week='mon,tue,wed,thu,fri,sat,sun', timezone=pytz.timezone('US/Eastern'))])
        second_AurorianCR_AM = AndTrigger([CronTrigger(hour=5, minute=4, day_of_week='mon,tue,wed,thu,fri,sat,sun', timezone=pytz.timezone('US/Eastern'))])
        third_AurorianCR_AM = AndTrigger([CronTrigger(hour=9, minute=4, day_of_week='mon,tue,wed,thu,fri,sat,sun', timezone=pytz.timezone('US/Eastern'))])

        self.scheduler.add_job(self.send_message, first_AurorianCR_PM)
        self.scheduler.add_job(self.send_message, second_AurorianCR_PM)
        self.scheduler.add_job(self.send_message, third_AurorianCR_PM)
        self.scheduler.add_job(self.send_message, firstAurorianCR_AM)
        self.scheduler.add_job(self.send_message, second_AurorianCR_AM)
        self.scheduler.add_job(self.send_message, third_AurorianCR_AM)



    async def send_message(self):
        channel = self.client.get_channel(event_Ping)  # replace with your channel ID
        embed = Embed(title="Crimson Rift **Auroria**", description="**Spawns in 15 Minutes**", color=0xff0000)
        embed.set_image(url="http://archeage.mablog.eu/wp-content/uploads/2018/09/ScreenShot0126.jpg")
        embed.set_thumbnail(
            url="https://1000logos.net/wp-content/uploads/2020/09/ArcheAge-logo.png")

        self.client.loop.create_task(channel.send("@everyone",embed=embed))

    @commands.Cog.listener()
    async def on_ready(self):
        print("Aurorian_Crimson_Rift_Notification Loaded")
        self.scheduler.start()


async def setup(client):
    await client.add_cog(AurorianCR(client))
