'''
Created on May 28, 2020

@author: Ron
'''
import discord
from discord.ext import commands, tasks
from itertools import cycle
from discord.utils import get
import youtube_dl
import os
import random

token = 'NzE1Mzc0OTk2MjEzNzI3MzYz.Xs_ggg.HQG0afQXizWV6LqyQpkaKRX6Sbw'
client = commands.Bot(command_prefix='.')
status = cycle(['Status 1', 'Status 2'])

players = {}


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Invalid command used.')
@client.event
async def on_ready():
#     await client.change_presence(status = discord.Status.idle, activity = discord.Game('Hiya!'))
    print('Bot online.')

@tasks.loop(seconds = 10)
async def change_status():
    change_status.start()
    await client.change_presence(status = discord.Status.idle, activity = discord.Game(next(status)))
    
    
@client.event 
async def on_member_join(member):
    print(f'{member} has joined a server.')
    

@client.event 
async def on_member_remove(member):
    print(f'{member} has left a server.')
    

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! Ping: {round(client.latency * 1000)}ms.')


@client.command()
async def shutdown(ctx):
    await ctx.bot.logout()
    
@client.command()
async def clear(ctx, amount = 2):
    await ctx.channel.purge(limit = amount)

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please specify the amount of messages to clear.')
    
@client.command(aliases=['8ball', 'test'])
# asterisk allows me to take in multiple parameters
async def _8ball(ctx, *, question):
    responses = ["It is certain.",
                "It is decidedly so.",
                "Without a doubt.",
                "Yes - definitely.",
                "You may rely on it.",
                "As I see it, yes.",
                "Most likely.",
                "Outlook good.",
                "Yes.",
                "Signs point to yes.",
                "Reply hazy, try again.",
                "Ask again later.",
                "Better not tell you now.",
                "Cannot predict now.",
                "Concentrate and ask again.",
                "Don't count on it.",
                "My reply is no.",
                "My sources say no.",
                "Outlook not so good.",
                "Very doubtful."]
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')
    
    
@client.command()
#asterisk - all parameters after member and reason will be added onto reason
async def kick(ctx, member : discord.Member, * , reason = None):
    await member.kick(reason = reason)
    
@client.command()
async def ban(ctx, member : discord.Member, * , reason = None):
    await member.ban(reason = reason)
    await ctx.send(f'Banned {member.mention}')    

@client.command()
# Ron#1234 where member_name is Ron and member_discriminator is 1234
async def unban(ctx, *, member):
    #guild is server, ban entries pulled from guild
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')
    
    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild(unban(user))
            await ctx.send(f'Unbanned {user.mention}') 

@client.command()
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild = ctx.guild)
    
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else: 
        voice = await channel.connect()
        print(f"The bot has connected to {channel}\n")

#     await voice.disconnect()
# 
#     if voice and voice.is_connected():
#         await voice.move_to(channel)
#     else:
#         voice = await channel.connect()
#         print(f"The bot has connected to {channel}\n")


@client.command()
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild = ctx.guild)
    if voice and voice.is_connected():
        await voice.disconnect()
        print(f'Bot disconnected from {channel}\n')
        await ctx.send(f'Left {channel}')
    else:
        print('Bot was not in voice channel')
        await ctx.send("Wasn't in a voice channel")
        
    
    
            
@client.command()
async def play (ctx,url):
  
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            print("Removed old song file")
    except PermissionError:
        print("Trying to delete song file, but it's being played")
        await ctx.send("Music's already playing")
        return

#     await ctx.send("Loading your song...")
    await ctx.send("Loading your anime OSTs...")

    voice = get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now\n")
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Renamed File: {file}\n")
            os.rename(file, "song.mp3")
            break

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print("Song done!"))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 1

#new name used for display
    nname = name.rsplit("-", 2)
    await ctx.send(f"Playing: {nname[0]}")
    print("playing\n")

@client.command()
async def stop(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("Music stopped")
        voice.stop()
        await ctx.send("Music stopped.")
    else:
        print("No music playing failed to stop")
        await ctx.send("There's no music playing. ")

@client.command()
async def pause(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("Music paused")
        voice.pause()
        await ctx.send("Music paused")
    else:
        print("Music not playing failed pause")
        await ctx.send("Music not playing...are you good?")
        
        
@client.command()
async def resume(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_paused():
        print("Resumed music")
        voice.resume()
        await ctx.send("Resumed music")
    else:
        print("Music is not paused")
        await ctx.send("Music not paused, don't waste my time.")

        
# insert token    
client.run(token)
