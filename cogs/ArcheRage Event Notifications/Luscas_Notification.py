import pytz
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.combining import AndTrigger

from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from discord import Embed

from main import event_Ping


class luscasTimer(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.scheduler = AsyncIOScheduler(timezone=pytz.timezone('US/Eastern'))
        self.scheduler.start()
        firstLuscas = AndTrigger([CronTrigger(hour=16, minute=14, day_of_week='mon,tue,wed,thu,fri,sat,sun', timezone=pytz.timezone('US/Eastern'))])
        secondLuscas = AndTrigger([CronTrigger(hour=20, minute=44, day_of_week='mon,tue,wed,thu,fri,sat,sun', timezone=pytz.timezone('US/Eastern'))])

        self.scheduler.add_job(self.send_message, firstLuscas)
        self.scheduler.add_job(self.send_message, secondLuscas)

    async def send_message(self):
        channel = self.client.get_channel(event_Ping)  # replace with your channel ID
        embed = Embed(title="Luscas Awakening", description="**Spawns in 15 Minutes**", color=0xff0000)
        embed.set_image(url="https://static.wikia.nocookie.net/archeage_gamepedia/images/e/e6/Luscas_Awakening.jpg/revision/latest/scale-to-width-down/1000?cb=20191203154420")
        embed.set_thumbnail(
            url="https://1000logos.net/wp-content/uploads/2020/09/ArcheAge-logo.png")

        self.client.loop.create_task(channel.send("@everyone",embed=embed))

    @commands.Cog.listener()
    async def on_ready(self):
        print("Luscas_Notification_Loaded")
        self.scheduler.start()


async def setup(client):
    await client.add_cog(luscasTimer(client))
