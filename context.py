import discord
from discord.ext import commands
import asyncio

class CustomContext(commands.Context):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

    async def _send(self, content=None, *, tts=False, embed=None, file=None, files=None, delete_after=None, nonce=None): #you fucking nonce - Ramsay
        #Helper function, do not call
        if file or files:
            return await super().send(content=content, tts=tts, embed=embed, file=file, files=files, delete_after=delete_after, nonce=nonce)
        
        msg = None
        l = await (self.channel.history(limit=15)).flatten()
        m = discord.utils.get(l,author=self.guild.me)
        if m:
            await m.edit(content=content, embed=embed, delete_after=delete_after)
            return m
        
        m = await super().send(content=content, tts=tts, embed=embed, file=file, files=files, delete_after=delete_after, nonce=nonce)
        return m

    async def send(self, content=None, *, tts=False, embed=None, file=None, files=None, delete_after=None, nonce=None, edit=False):
        ctxpass = False
        for x in self.args:
            print(x.kwargs)
            if str(x) == "edit" and self.kwargs[x] == True:
                ctxpass = True
        if edit or ctxpass:
            return await self._send(content=content, tts=tts, embed=embed, file=file, files=files, delete_after=delete_after, nonce=nonce)

        return await super().send(content=content, tts=tts, embed=embed, file=file, files=files, delete_after=delete_after, nonce=nonce)

