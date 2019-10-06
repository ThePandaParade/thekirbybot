from discord.ext import commands
import json
import aiohttp
import asyncio

with open('tokens.json') as f:
    tokens = json.load(f)
class dbl(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = self.bot.session
        self.token = tokens["botlists"]["dbl"]
        self.bot.loop.create_task(self.on_ready())

    # def __unload(self):
    #     self.bot.loop.create_task(self.session.close())

    async def send(self):
        dump = json.dumps({
            'server_count': len(self.bot.guilds)
            #'server_count': 235
        })
        head = {
            'authorization': self.token,
            'content-type' : 'application/json'
        }
        
        url = 'https://discordbots.org/api/bots/508268149561360404/stats'

        async with self.bot.session.post(url, data=dump, headers=head) as resp:
            print('returned {0.status} for {1} on dbl'.format(resp, dump))
            await self.bot.get_channel(581803242992697346).send("**DBL:** Returned {0.status} for {1}".format(resp, dump))


    async def on_ready(self):
        while True:
            await self.send()
            await asyncio.sleep(1800)

def setup(bot):
    bot.add_cog(dbl(bot))