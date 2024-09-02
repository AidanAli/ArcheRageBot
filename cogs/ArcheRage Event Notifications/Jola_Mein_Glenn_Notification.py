import pytz
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.combining import AndTrigger

from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from discord import Embed

from main import event_Ping


class JMG(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.scheduler = AsyncIOScheduler(timezone=pytz.timezone('US/Eastern'))
        self.scheduler.start()
        JMG_1 = AndTrigger([CronTrigger(hour=15, minute=4, day_of_week='mon,tue,wed,thu,fri,sat,sun', timezone=pytz.timezone('US/Eastern'))])
        JMG_2 = AndTrigger([CronTrigger(hour=7, minute=4, day_of_week='mon,tue,wed,thu,fri,sat,sun', timezone=pytz.timezone('US/Eastern'))])
        JMG_3 = AndTrigger([CronTrigger(hour=11, minute=4, day_of_week='mon,tue,wed,thu,fri,sat,sun', timezone=pytz.timezone('US/Eastern'))])
        self.scheduler.add_job(self.send_message, JMG_1)
        self.scheduler.add_job(self.send_message, JMG_2)
        self.scheduler.add_job(self.send_message, JMG_3)

    async def send_message(self):
        channel = self.client.get_channel(event_Ping)  # replace with your channel ID
        embed = Embed(title="Jola Meina/Glenn", description="**Spawns in 15 Minutes**", color=0xff0000)
        embed.set_image(url="https://oyster.ignimgs.com/mediawiki/apis.ign.com/archeage/4/47/Meina.jpg?width=640")
        embed.set_thumbnail(
            url="https://1000logos.net/wp-content/uploads/2020/09/ArcheAge-logo.png")

        self.client.loop.create_task(channel.send("@everyone",embed=embed))

    @commands.Cog.listener()
    async def on_ready(self):
        print("Jola_Mein_Glenn_Notification Loaded")
        self.scheduler.start()


async def setup(client):
    await client.add_cog(JMG(client))
