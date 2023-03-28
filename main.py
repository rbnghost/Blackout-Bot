#discord pkg importieren
import discord
from discord.ext import commands

#benutzerdefinierte pakete importieren
from utils.readconfig import readconfig
from functions.getcoins import getcoins
from functions.coinschanger import addcoins, remcoins
from functions.slotsystem import playslot
import utils.config as config

# Konfigurationsdatei laden
config.data = readconfig("./config.json")


# Discord-Bot-Objekt initialisieren
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix=config.data['prefix'], intents=intents)

# Debugging-Optionen definieren
@client.command()
async def add(ctx, amount, member: discord.Member = None):
    try:
        amount = int(amount)
        # Benutzer-ID definieren, um das Guthaben in der Coins-Liste zuzuordnen
        
        if member:
            user_id = str(member.id)
            # Coins-Liste aus der Datei laden und Coins hinzufügen
            try:
                addcoins(user_id, amount)
                await ctx.send(f"{member} wurde {amount} coin hinzugefügt!")
            except:
                await ctx.send(f"Es ist ein Fehler Aufgetreten, Überprüfe ob deine Zahl gültig ist.")
        else:
            user_id = str(ctx.author.id)
            # Coins-Liste aus der Datei laden und Coins hinzufügen
            try:
                addcoins(user_id, amount)
                await ctx.send(f"You got {amount} coin for free!")
            except:
                await ctx.send(f"Es ist ein Fehler Aufgetreten, Überprüfe ob deine Zahl gültig ist.")
    except:
        pass

@client.command()
async def rem(ctx, amount, member: discord.Member = None):
    try:
        amount = int(amount)
        # Benutzer-ID definieren, um das Guthaben in der Coins-Liste zuzuordnen
        user_id = str(ctx.author.id)
        if member:
            user_id = str(member.id)
            # Coins-Liste aus der Datei laden und Coins entfernen
            try:
                remcoins(user_id, amount)
                # Antwort im Discord senden
                await ctx.send(f"{member} wurde {amount} coin entfernt!")
            except:
                await ctx.send(f"Es ist ein Fehler Aufgetreten, Überprüfe ob deine Zahl gültig ist.")
        else:
            user_id = str(ctx.author.id)
            # Coins-Liste aus der Datei laden und Coins hinzufügen
            try:
                remcoins(user_id, amount)
                await ctx.send(f"You got {amount} coin removed!")
            except:
                await ctx.send(f"Es ist ein Fehler Aufgetreten, Überprüfe ob deine Zahl gültig ist.")
    except:
        pass

@client.command()
async def coins(ctx, member: discord.Member = None):
    # Benutzer-ID definieren, um das Guthaben in der Coins-Liste zuzuordnen
    user_id = str(ctx.author.id)
    if member:
        user_id = str(member.id)
    # Coins-Liste aus der Datei laden und das Guthaben des Benutzers abrufen
    coins = getcoins(config.data["coinsfile"])
    usercoins = coins[user_id]
    # Antwort im Discord senden
    await ctx.send(f"You got {usercoins} coin")

@client.command()
async def slot(ctx, amount):
    try:
        amount = int(amount)
        # Benutzer-ID definieren, um das Guthaben in der Coins-Liste zuzuordnen
        user_id = str(ctx.author.id)
        # Slot-Spiel durchführen
        result = playslot(amount, user_id)
        # Antwort im Discord senden
        await ctx.send(result)
    except:
        pass

# Bot mit dem Token starten
client.run(config.data['token'])
