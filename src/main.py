import urllib.parse
import urllib.request
import re
import musiclib as music
from asyncio.windows_events import NULL
import discord
from discord.utils import get
import youtube_dl
from discord import channel
from discord import message
from discord.errors import ClientException
from discord.ext import commands
import random
import response
import api 
from discord import FFmpegPCMAudio

yt = api.YoutubeSearch()

bot = discord.Client()
bot = commands.Bot(command_prefix='.')
connect = False
voice_client = music.voice()


@bot.event
async def on_ready():
    print('logged in as {0.user}'.format(bot))


@bot.command()
async def vanakkam(ctx):
    await ctx.send('Vanakkam nanbargaley'+ctx.author.mention)


@bot.command()
async def kaatu(ctx, user=""):
    await ctx.send("Poi maatu saaniya paarule {0}".format(str(user)))


@bot.command()
async def sollu(ctx, args, num=1):
    await ctx.send((str(args) + "\n")*int(num))


@bot.command()
async def nakku(ctx, arg=""):
    embed = discord.Embed()

    embed.set_image(
        url="https://media1.tenor.com/images/1bd1a71b7e6a15b116638e90695ecc0f/tenor.gif?itemid=20326152")
    await ctx.send(embed=embed)
    await ctx.send(str(arg))


@bot.command()
async def truthabout(ctx, arg):

    #   embed = discord.Embed()
    #    embed.set_image(
    #       url="https://media1.tenor.com/images/9a94ccad1586c72f01020b24c2dae034/tenor.gif?itemid=21659407")
    index = random.randint(0, len(response.truth)-1)
    await ctx.send(response.truth[index]+" "+str(arg))
#   await ctx.send(embed=embed)


@bot.command()
async def gudnit(ctx, usr=""):
    embed = discord.Embed()
    embed.set_image(
        url="https://img.dtnext.in/Articles/2020/Oct/202010102053533815_Tiktok-fame-GP-Muthu-attempts-suicide-admitted-to-hospital_SECVPF.gif")
    await ctx.send("GUD NIT {0}".format(str(usr)))
    await ctx.send(embed=embed)


@bot.command()
async def hi(ctx):
    await ctx.send("vaa le sethapayale "+ctx.author.mention)


@bot.command(pass_context=True)
async def send(ctx, arg):
    try:
        await ctx.send(str(arg))
        await ctx.send("https://www.youtube.com/watch?v=y5PccRMn-nI&ab_channel=GpmuthuPacific")
    except:
        await ctx.send("You must tag someone to use this command")


@bot.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)

# joining voice joining channel
@bot.command()
async def join(ctx):
    await voice_client.ajoin(ctx)

# leaving a channel
@bot.command()
async def leave(ctx):
    await voice_client.leave(ctx)

@bot.command()
async def play(ctx, *args):
    keyword = ""
    for arg in args :
        keyword += arg
    print(keyword)
    url = voice_client.search(keyword)
    await voice_client.aplay(ctx, url)


@bot.command()
async def pause(ctx):
    await voice_client.apause(ctx)


@bot.command()
async def resume(ctx):
    await voice_client.aresume(ctx)


@bot.command()
async def stop(ctx):
    await voice_client.astop(ctx)

@bot.command()
async def search(ctx,*args,num = 6):
    keyword = ""
    for arg in args :
        keyword += str(arg)
    results =  voice_client.search(search =keyword,option = 1,totalResults=num)
    task =  await voice_client.displaySearchResult(ctx,result=results)
    print(results)

@bot.command()
async def choose(ctx,choice):
    url = "https://www.youtube.com/watch?v="+voice_client.video_ids[choice]
    await voice_client.aplay(ctx,url)

@bot.command(describe = "Play raavu audio ")
async def raavu(ctx, arg=""):
    await voice_client.audio(file_path=r"music\bgmsaavu.mp3", ctx=ctx, arg=arg)

# saavu command plays an audio
@bot.command()
async def saavu(ctx, arg=""):
    await voice_client.audio(file_path=r"music\sethapayale.mp3", ctx=ctx, arg=arg)


@bot.command()
async def poyamle(ctx, arg=""):
    await voice_client.audio(file_path=r"music\poyamle.mp3", ctx=ctx, arg=arg)


token = 'ODU0MDA0MjAyOTIxMDAwOTkw.YMdnZA.s0OwdF6Sy0oQ6shpvfYBsTsHmYs'
bot.run(token)
