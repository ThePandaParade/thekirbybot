from discord.ext import commands
import json
import aiohttp
import asyncio

with open('tokens.json') as f: # Could use envs, but hopefully someone might land up PRing that.
    tokens = json.load(f)
class ddb(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = self.bot.session
        self.token = tokens["botlists"]["ddb"]
        self.bot.loop.create_task(self.on_ready())

    # def __unload(self):
    #     self.bot.loop.create_task(self.session.close())

    async def send(self):
        dump = json.dumps({
            'server_count': len(self.bot.guilds)
            #'server_count': 258
        })
        head = {
            'authorization': self.token,
            'content-type' : 'application/json'
        }
        
        url = 'https://divinediscordbots.com/bot/508268149561360404/stats'

        async with self.bot.session.post(url, data=dump, headers=head) as resp:
            print('returned {0.status} for {1} on ddb'.format(resp, dump))
            await self.bot.get_channel(632269137711726592).send("**DDB:** Returned {0.status} for {1}".format(resp, dump))


    async def on_ready(self):
        while True:
            await self.send()
            await asyncio.sleep(1800)

def setup(bot):
    bot.add_cog(ddb(bot))