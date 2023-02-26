import discord
from discord.ext import commands
import random 
import json
import os
from datetime import datetime, timedelta

TOKEN = 'Token here'

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='"', intents=intents)

user_cooldowns = {}

COOLDOWN_FILE = "cooldowns.json"

DAILY_REWARD = 300

def load_cooldowns():
    if os.path.exists(COOLDOWN_FILE):
        with open(COOLDOWN_FILE) as f:
            return json.load(f)
    return {}

def save_cooldowns():
    with open(COOLDOWN_FILE, 'w') as f:
        json.dump(user_cooldowns, f)
        
def cooldown_15_minutes():
    async def predicate(ctx):
        user_id = str(ctx.author.id)
        if user_id in user_cooldowns:
            last_time = datetime.fromisoformat(user_cooldowns[user_id])
            if datetime.utcnow() - last_time < timedelta(minutes=15):
                await ctx.send("You can only use this command once every 15 minutes.")
                return False
        user_cooldowns[user_id] = datetime.utcnow().isoformat()
        save_cooldowns()
        return True
    return commands.check(predicate)

def cooldown_10_minutes():
    async def predicate(ctx):
        user_id = str(ctx.author.id)
        if user_id in user_cooldowns:
            last_time = datetime.fromisoformat(user_cooldowns[user_id])
            if datetime.utcnow() - last_time < timedelta(minutes=10):
                await ctx.send("You can only use this command once every 10 minutes.")
                return False
        user_cooldowns[user_id] = datetime.utcnow().isoformat()
        save_cooldowns()
        return True
    return commands.check(predicate)

def save_coins(user_id, amount=0):
    try:
        with open('coins.json', 'r') as f:
            coins = json.load(f)
    except FileNotFoundError:
        coins = {}

    if user_id not in coins:
        coins[user_id] = 0

    coins[user_id] += amount

    with open('coins.json', 'w') as f:
        json.dump(coins, f)

    return coins[user_id]

@client.command()
@cooldown_15_minutes()
async def roll(ctx):
    number1 = random.randint(1,6)
    number2 = random.randint(1,6)
    number3 = random.randint(1,6)
    number4 = random.randint(1,6)
    number5 = random.randint(1,6)

    await ctx.send(f'Your Numbers are: {number1}, {number2}, {number3}, {number4}, {number5}')

@client.event
async def on_ready():
    global user_cooldowns
    user_cooldowns = load_cooldowns()

@client.event
async def on_disconnect():
    save_cooldowns()

def get_coins():
    with open('coins.json', 'r') as f:
        coins = json.load(f)
    return coins

@client.command()
async def coins(ctx):
    user_id = str(ctx.author.id)
    coins = get_coins().get(user_id, 0)
    await ctx.send(f"You currently have {coins} coins.")

@client.command()
async def free(ctx):
    user_id = str(ctx.author.id)
    coins = get_coins()

    if user_id in coins:
        coins[user_id] += 1
    else:
        coins[user_id] = 1

    with open('coins.json', 'w') as f:
        json.dump(coins, f)

    await ctx.send(f"You got 1 coin for free!")

@client.command()
async def shop(ctx):
    coins = get_coins().get(str(ctx.author.id), 0)
    embed = discord.Embed(title="Shop", description=f"You currently have {coins} coins.", color=0x00ff00)
    embed.add_field(name="Bronze Rank", value="Cost: 100 coins")
    embed.add_field(name="Silver Rank", value="Cost: 500 coins")
    embed.add_field(name="Gold Rank", value="Cost: 1000 coins")
    embed.set_footer(text="To purchase a rank, use the command 'buy <rank>'.")
    await ctx.send(embed=embed)

@client.command()
async def buy(ctx, *, rank):
    coins = get_coins()
    user_id = str(ctx.author.id)
    if user_id not in coins:
        coins[user_id] = 0
    if rank.lower() == "bronze":
        if coins[user_id] >= 100:
            coins[user_id] -= 100
            await ctx.send(f"You have purchased the Bronze Rank for 100 coins!")
            save_coins(coins)
        else:
            await ctx.send("You do not have enough coins to purchase this rank.")
    elif rank.lower() == "silver":
        if coins[user_id] >= 500:
            coins[user_id] -= 500
            await ctx.send(f"You have purchased the Silver Rank for 500 coins!")
            save_coins(coins)
        else:
            await ctx.send("You do not have enough coins to purchase this rank.")
    elif rank.lower() == "gold":
        if coins[user_id] >= 1000:
            coins[user_id] -= 1000
            await ctx.send(f"You have purchased the Gold Rank for 1000 coins!")
            save_coins(coins)
        else:
            await ctx.send("You do not have enough coins to purchase this rank.")
    else:
        await ctx.send("That rank is not available in the shop.")
    
coins = {}
@client.command()
@cooldown_10_minutes()
async def slot(ctx):
    user_id = str(ctx.author.id)
    liste = ["💣", "💰", "💎", "💸","⌚️","❤️", "🔔", "♠️"]
    symbol1 = (random.choice(liste))
    symbol2 = (random.choice(liste))
    symbol3 = (random.choice(liste))
    await ctx.send(f"{symbol1}, {symbol2}, {symbol3}")
    
    if symbol1 == symbol2 == symbol3:
        coins[user_id] = coins.get(user_id, 0) + 500
        await ctx.send("You get 500 Coins!")
       
    elif symbol1 == symbol2 or symbol2 == symbol3 or symbol1 == symbol3:
        coins[user_id] = coins.get(user_id, 0) + 150
        await ctx.send("You get 150 Coins!")
        
    else: 
        await ctx.send("You didn't win")
    with open('coins.json', 'w') as f:
        json.dump(coins, f)

client.run(TOKEN)
