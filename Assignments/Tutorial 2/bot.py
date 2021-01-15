# Developed by Stan

import os

import discord
import time
from discord.ext import commands
from dotenv import load_dotenv

# Load in environment variables, set up client
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN').strip('{}')
GUILD = os.getenv('DISCORD_GUILD').strip('{}')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='.wongbot', intents=intents)

# Initialize currency system
user_amounts = {}

# Runs once bot is connected and available.
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

    guild = discord.utils.get(bot.guilds, name=GUILD)

    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    try:
        with open('user_amounts.json') as f:
            user_amounts = json.load(f)
    except FileNotFoundError:
        print("Could not load user_amounts.json")
        user_amounts = {}

    # members = '\n - '.join([member.name for member in guild.members])
    # print(f'Guild Members:\n - {members}')

@bot.event
async def on_member_join(member):
    guild = discord.utils.get(bot.guilds, name=GUILD)
    general = discord.utils.get(guild.channels, name='general')
    print(general.name)
    await general.send(
        f'{member.name} HAS BEEN ASSIMILATED.'
    )

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.error.CheckFailure):
        await ctx.send('WHERE TF ARE YOUR PERMISSIONS BOYO')
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('INVALID COMMAND DIPSHIT.')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.content == 'wongbot awaken':
        await message.channel.send(f'WONGBOT ACTIVATED')
    
    if 'casino' in message.content:
        await message.channel.send(f'CASINO UNDER DEVELOPMENT')

    if 'anime' in message.content:
        await message.channel.send(f'NO ANIME ALLOWED. BAN COMMENCING IN 10 SECONDS')
        guild = discord.utils.get(bot.guilds, name=GUILD)
        offender = discord.utils.get(guild.members, name=message.author)
        for i in range(10, -1, -1):
            await message.channel.send(content=str(i), delete_after=1)
            time.sleep(1)
        await message.channel.send(f"TIME'S UP, GOODBYE WEEB", delete_after=2)

        #await guild.ban(message.author, reason='WEEB DETECTED', delete_message_days=0)
        await guild.kick(message.author)
        #await offender.edit(voice_channel=None)
        await message.channel.send(f'{message.author} REMOVED, GOOD WORK TEAM')

    if 'catgirl' in message.content:
        await message.channel.send(f'NO CATGIRLS ALLOWED. BAN COMMENCING IN 10 SECONDS')   


############################
##### ECONOMY COMMANDS #####
############################

@bot.command(pass_context=True)
async def balance(ctx):
    id = str(ctx.message.author.id)
    if id in user_amounts:
        await ctx.send("BALANCE: {} STANBUCKS".format(user_amounts[id]))
    else:
        await ctx.send("NO ACCOUNT. REGISTER WITH '.WONGBOT REGISTER'")

@bot.command(pass_context=True)
async def register(ctx):
    id = str(ctx.message.author.id)
    if id not in user_amounts:
        user_amounts[id] = 10,000
        await ctx.send("REGISTER SUCCESSFUL")
        _save()
    else:
        await ctx.send("YOU ALREADY HAVE AN ACCOUNT NICE TRY")

@bot.command(pass_context=True)
async def transfer(ctx, amount: int, other: discord.Member):
    primary_id = str(ctx.message.author.id)
    other_id = str(other.id)
    if primary_id not in user_amounts:
        await ctx.send("NO ACCOUNT. REGISTER WITH '.WONGBOT REGISTER'")
    elif other_id not in amounts:
        await ctx.send("OTHER PARTY DOES NOT HAVE AN ACCOUNT.")
    elif user_amounts[primary_id] < amount:
        await ctx.send("NO OVERDRAFTING GTFO")
    else:
        user_amounts[primary_id] -= amount
        user_amounts[other_id] += amount
        await ctx.send("TRANSACTION COMPLETED")
    _save()

def _save():
    with open('user_amounts.json', 'w+') as f:
        json.dump(user_amounts, f)

@bot.command()
async def save():
    _save()

@bot.command(name='bet', help='bet stanbucks against ur friends')
async def bet(ctx):
    pass

# Begin bot session
bot.run(TOKEN)