import re
import discord
import urllib.parse
import urllib.request
from discord.errors import ClientException
import youtube_dl
import api
 
yt = api.YoutubeSearch()

class voice:
    __connect = False
    __vc = None

#To join a voice channel
    async def ajoin(self, ctx):
        channel = ctx.author.voice
        if channel != None and self.__connect != True:
            self.__vc = await channel.channel.connect()
            self.__connect = True
        elif(self.__connect == True):
            await ctx.send("Already connected to some Voice channel try \".leave\" and \".join\"")
        else:
            await ctx.send("You are not connected to a voice channel")
            
#to leave a voice channel
    async def leave(self, ctx):
        channel = ctx.author.voice.channel
        if(self.__connect == True):
            await ctx.voice_client.disconnect()
            self.__connect = False
        else:
            await ctx.send("Not connect to any channel")

#to play an audio from a passed url 
    async def aplay(self, ctx, url):

        channel = ctx.author.voice
        if channel == None:
            await ctx.send("@"+str(ctx.author.name) + " you are not in a channel.")
            return
        elif(self.__connect and channel != None):
            await ctx.send(" now playing ")
            await ctx.send(url)
            ydl_opts = {'format': 'bestaudio'}
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                URL = info['formats'][0]['url']
            #voice = get(ctx.bot.voice_clients, guild=ctx.guild)
            self.__vc.play(discord.FFmpegPCMAudio(
                executable=r"ffmpeg.exe", source=URL))
        elif(self.__connect == False):
            task = await self.ajoin(ctx)
            await self.aplay(ctx, url)
            return

#to play a audio file frm local storage
    async def audio(self, file_path, ctx):
        channel = ctx.author.voice
        if channel == None:
            await ctx.send("@"+str(ctx.author.name) + " you are not in a channel.")
            return
        elif(self.__connect and channel != None):
            self.__vc.play(discord.FFmpegPCMAudio(executable=r"ffmpeg.exe",
                                                  source=file_path))
        elif(self.__connect == False):
            task = await self.ajoin(ctx)
            await self.audio(file_path, ctx)
            return

#to pause a audio
    async def apause(self, ctx):
        try:
            self.__vc.pause()
        except:
            await ctx.send("Not playing anything rn")

#to stop a playing audio
    async def astop(self, ctx):
        try:
            self.__vc.stop()
        except:
            await ctx.send("Not playing anything rn")

#to resume a playing audio
    async def aresume(self, ctx):
        try:
            self.__vc.resume()
        except:
            await ctx.send("Not playing anything rn")

#returns a url relate to the keyword entered
    #def search(self, search,option = 0):
    #        search_keyword = search
     #       html = urllib.request.urlopen(
    #         "https://www.youtube.com/results?search_query=" + search_keyword)
    #        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    #        if option == 0:
    #            return "https://www.youtube.com/watch?v=" + video_ids[0]
     #       elif option == 1: 
    #            return video_ids
                
    def search(self, search,option = 0,totalResults = 4):
            search_keyword = search
            html = urllib.request.urlopen(
                "https://www.youtube.com/results?search_query=" + search_keyword)
            video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
            if option == 0:
                return "https://www.youtube.com/watch?v=" + video_ids[0]
            elif option == 1: 
                return yt.startSearch(video_ids,totalResults)


    async def displaySearchResult(self,ctx,result):
        index = 0 
        for row in result:
            
            for colomn in row:
                task = await ctx.send(f'[{index}]'+colomn)
            index+=1   
        return
            