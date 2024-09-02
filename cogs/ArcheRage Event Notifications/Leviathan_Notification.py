import pytz
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.combining import AndTrigger

from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from discord import Embed

from main import event_Ping


class LeviTimer(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.scheduler = AsyncIOScheduler(timezone=pytz.timezone('US/Eastern'))
        self.scheduler.start()
        monLevi = AndTrigger([CronTrigger(hour=19, minute=49, day_of_week='mon', timezone=pytz.timezone('US/Eastern'))])
        wedLevi = AndTrigger([CronTrigger(hour=19, minute=49, day_of_week='wed', timezone=pytz.timezone('US/Eastern'))])
        friLevi= AndTrigger([CronTrigger(hour=19, minute=49, day_of_week='fri', timezone=pytz.timezone('US/Eastern'))])

        self.scheduler.add_job(self.send_message, monLevi)
        self.scheduler.add_job(self.send_message, wedLevi)
        self.scheduler.add_job(self.send_message, friLevi)

    async def send_message(self):
        channel = self.client.get_channel(event_Ping)  # replace with your channel ID
        embed = Embed(title="Leviathan Battle", description="levi Spawns in 15 Minutes", color=0xff0000)
        embed.set_image(url="https://preview.redd.it/92hvvqtj96d21.jpg?width=1920&format=pjpg&auto=webp&v=enabled&s=6bb304e42809cd456709807f51915f6fc6787553")
        embed.set_thumbnail(
            url="https://1000logos.net/wp-content/uploads/2020/09/ArcheAge-logo.png")

        self.client.loop.create_task(channel.send("@everyone",embed=embed))

    @commands.Cog.listener()
    async def on_ready(self):
        print("Leviathan_Notification Loaded")
        self.scheduler.start()


async def setup(client):
    await client.add_cog(LeviTimer(client))
