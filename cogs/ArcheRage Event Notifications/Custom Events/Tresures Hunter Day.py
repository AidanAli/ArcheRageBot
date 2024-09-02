import pytz
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.combining import AndTrigger

from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from discord import Embed

from main import event_Ping


class Treasure_Hunt_Event(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.scheduler = AsyncIOScheduler(timezone=pytz.timezone('US/Eastern'))
        self.scheduler.start()
        Merchants_Day = AndTrigger([CronTrigger(hour=23, minute=44, day_of_week='wed', timezone=pytz.timezone('US/Eastern'))])
        self.scheduler.add_job(self.send_message, Merchants_Day)

    async def send_message(self):
        channel = self.client.get_channel(event_Ping)  # replace with your channel ID
        embed = Embed(title="Treasures Hunter Day!", description="Started ! Grab your Quests", color=0x00FF00)
        embed.set_image(url="https://i.ibb.co/wMLfv39/37rByVp.png")
        embed.set_thumbnail(
            url="https://1000logos.net/wp-content/uploads/2020/09/ArcheAge-logo.png")
        embed.add_field(
            name="Event Details",value="https://na.archerage.to/forums/threads/game-event-treasures-hunter-day.8637/")

        self.client.loop.create_task(channel.send(embed=embed))

    @commands.Cog.listener()
    async def on_ready(self):
        print("Treasure_Hunt_ Loaded")
        self.scheduler.start()


async def setup(client):
    await client.add_cog(Treasure_Hunt_Event(client))
