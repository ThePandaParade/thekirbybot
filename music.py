import logging
import math
import re
import random
import discord
import lavalink
from discord.ext import commands

time_rx = re.compile('[0-9]+')
url_rx = re.compile('https?:\/\/(?:www\.)?.+')  # noqa: W605
emojis = [591742564223156254,591742564571545628,555131286360948741,555131287736680452]


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        if not hasattr(self.bot, 'lavalink'):
            self.bot.lavalink = lavalink.Client(bot.user.id)
            self.bot.lavalink.add_node(password='bananaboy21',port=2333,host="159.203.28.34",region="us")  # Host, Port, Password, Region, Name
            self.bot.add_listener(bot.lavalink.voice_update_handler, 'on_socket_response')

    def cog_unload(self):
        self.bot.lavalink._event_hooks.clear()

    async def cog_before_invoke(self, ctx):
        guild_check = ctx.guild is not None
        #  This is essentially the same as `@commands.guild_only()`
        #  except it saves us repeating ourselves (and also a few lines).

        if guild_check:
            await self.ensure_voice(ctx)
            #  Ensure that the bot and command author share a mutual voicechannel.

        return guild_check

    async def track_hook(self, event):
        if isinstance(event, lavalink.events.QueueEndEvent):
            guild_id = int(event.player.guild_id)
            await self.connect_to(guild_id, None)
            # Disconnect from the channel -- there's nothing else to play.

    async def connect_to(self, guild_id: int, channel_id: str):
        """ Connects to the given voicechannel ID. A channel_id of `None` means disconnect. """
        ws = self.bot._connection._get_websocket(guild_id)
        await ws.voice_state(str(guild_id), channel_id)
        # The above looks dirty, we could alternatively use `bot.shards[shard_id].ws` but that assumes
        # the bot instance is an AutoShardedBot.

    @commands.command(name='play', aliases=['p','music'])
    @commands.guild_only()
    async def _play(self, ctx, *, query: str):
        player = self.bot.lavalink.players.get(ctx.guild.id)

        query = query.strip('<>')

        if not url_rx.match(query):
            query = f'ytsearch:{query}'

        results = await player.node.get_tracks(query)

        if not results or not results['tracks']:
            return await ctx.send('Nothing found! Did the hamsters crash? Did you make a typo? Is youtube down? Nobody knows...')


        if results['loadType'] == 'PLAYLIST_LOADED':
            tracks = results['tracks']

            for track in tracks:
                player.add(requester=ctx.author.id, track=track)

            await ctx.send(f'Enqueued {len(tracks)} songs from {results["playlistInfo"]["name"]}')
        else:
            track = results['tracks'][0]
            await ctx.send(f"Added ``{track['info']['title']}`` to the queue")
            player.add(requester=ctx.author.id, track=track)

        

        if not player.is_playing:
            await ctx.send(f"Now playing ``{track['info']['title']}`` {discord.utils.get(bot.emojis,id=random.choice(emojis))}")
            await player.play()



    @commands.command(name='skip', aliases=['s'])
    @commands.guild_only()
    async def _skip(self, ctx):
        """ Skips the current video"""
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not player.is_playing:
            return await ctx.send('I\'m not playing anything, silly. ')

        await player.skip()
        await ctx.send('Skipped the song. Woosh!')

    @commands.command(name='stop')
    @commands.guild_only()
    async def _stop(self, ctx):
        """ Stops the player and clears its queue. """
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not player.is_playing:
            return await ctx.send('I\'m not playing anything, silly. ')

        player.queue.clear()
        await player.stop()
        await ctx.send('Stopped the music and cleared the queue.')

    @commands.command(name='np', aliases=['n', 'playing'])
    @commands.guild_only()
    async def _np(self, ctx):
        """ Shows some stuff about the now playing song"""
        player = self.bot.lavalink.players.get(ctx.guild.id)
        song = 'Silence... In other words, nothing.'

        if player.current:
            position = lavalink.Utils.format_time(player.position)
            if player.current.stream:
                duration = 'Comin at ya live from Youtube'
            else:
                duration = lavalink.Utils.format_time(player.current.duration)
            song = f'**[{player.current.title}]({player.current.uri})**\n({position}/{duration})'

        embed = discord.Embed(color=discord.Color.blurple(), title='Now Playing', description=song)
        await ctx.send(embed=embed)

    @commands.command(name='queue', aliases=['q'])
    @commands.guild_only()
    async def _queue(self, ctx, page: int = 1):
        """ Shows the player's queue. """
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not player.queue:
            return await ctx.send('There\'s nothing in the queue! Why not keep the party up?')

        i = 0
        queue_fmt = []
        for s in player.queue:
            i = i + 1
            queue_fmt.append(f"{i}: {player.queue[i - 1].title}")
        
        
        queue_fmt = "\n".join(queue_fmt)
        await ctx.send(f"Queue for **{ctx.guild.name}**:\n\n```{queue_fmt}```")

    @commands.command(name='pause', aliases=['resume'])
    @commands.guild_only()
    async def _pause(self, ctx):
        """ Pauses/Resumes the current video. """
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not player.is_playing:
            return await ctx.send('I\'m not playing anything, silly. ')

        if player.paused:
            await player.set_pause(False)
            await ctx.send('⏯ | Resumed')
        else:
            await player.set_pause(True)
            await ctx.send('⏯ | Paused')

#    @commands.command(name='volume', aliases=['vol'])
#    @commands.guild_only()
#    async def _volume(self, ctx, volume: int = None):
#        """ Changes the player's volume. Must be between 0 and 150. Error Handling for that is done by Lavalink. """
#        player = self.bot.lavalink.players.get(ctx.guild.id)
#
#        if not volume:
#            return await ctx.send(f'🔈 | {player.volume}%')
#
#        await player.set_volume(volume)
#        await ctx.send(f'🔈 | Set to {player.volume}%')

    @commands.command(name='shuffle')
    @commands.guild_only()
    async def _shuffle(self, ctx):
        """ Shuffles the player's queue. """
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not player.is_playing:
            return await ctx.send('Nothing playing, silly.')

        player.shuffle = not player.shuffle
        await ctx.send(f'Shuffle {("enabled" if player.shuffle else "disabled")} for **{ctx.message.guild}**')

    @commands.command(name='repeat', aliases=['loop'])
    @commands.guild_only()
    async def _repeat(self, ctx):
        """ Repeats the current song until it's disabled """
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not player.is_playing:
            return await ctx.send('Nothing is playing, silly.')

        player.repeat = not player.repeat
        await ctx.send(f'Repeat {("enabled" if player.repeat else "disabled")} for **{ctx.message.guild}**')


    @commands.command(name='disconnect', aliases=['dc'])
    @commands.guild_only()
    async def _disconnect(self, ctx):
        """ Disconnects the bot from the VC"""
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not player.is_connected:
            return await ctx.send('I\'m not connected to a VC. How am I meant to leave?')

        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            return await ctx.send('You\'re not in my VC! I refuse to obey')

        player.queue.clear()
        await player.disconnect()
        await ctx.send('Disconnected from the VC and cleared the queue.')

    @_play.before_invoke
    async def ensure_voice(self, ctx):
        """ A few checks to make sure the bot can join a voice channel. """
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not player.is_connected:
            if not ctx.author.voice or not ctx.author.voice.channel:
                return await ctx.send(f'You are not in any VC, I can\'t play music in general, silly. ')
                

            permissions = ctx.author.voice.channel.permissions_for(ctx.me)

            if not permissions.connect or not permissions.speak:
                return await ctx.send('Um, so I am missing permissions to connect/speak in the channel you are in. Please ask a person to change my permissions.')

            player.store('channel', ctx.channel.id)
            await player.connect(ctx.author.voice.channel.id)
        else:
            if player.connected_channel.id != ctx.author.voice.channel.id:
                return await ctx.send('Join my voice channel!')
 

def setup(bot):
    bot.add_cog(Music(bot))