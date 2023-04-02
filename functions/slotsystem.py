import json

import random
from functions.getcoins import getcoins

import utils.config as config
from utils.validnum import positive

# Liste von Symbolen, die auf den Rollen des Spielautomaten angezeigt werden können
symb = [":cherries:", ":lemon:", ":tangerine:", ":bell:", ":cocktail:"]
# Wert jedes Symbols, wenn es in einer Gewinnlinie landet
values = {":cherries:": 3, ":lemon:": 4, ":tangerine:": 5, ":bell:": 6, ":cocktail:": 7}


def playslot(amount, user_id):
    # Lade die Anzahl der Münzen des Benutzers aus einer JSON-Datei
    coins = getcoins(config.data["coinsfile"])
    
    # Wenn der Einsatz höher ist als die Anzahl der Münzen des Benutzers, gib eine Fehlermeldung zurück
    if  amount > coins[user_id]:
        result = "you dont have enough coins"
        return result
    
    # Wenn der Einsatz ungültig ist, gib eine Fehlermeldung zurück
    if not positive(amount):
        result = "Ungültige nummer"
        return result
    
    # Zufällige Auswahl von Symbolen für die drei Rollen
    spin1 = random.choice(symb)
    spin2 = random.choice(symb)
    spin3 = random.choice(symb)
    
    # Überprüfen, ob alle drei Symbole gleich sind und berechne den Gewinn entsprechend
    if spin1 == spin2 == spin3:
        winnings = values[spin1] * amount
        result = f"You won {winnings} chips!\n{spin1} {spin2} {spin3}"
    # Überprüfen, ob zwei der Symbole gleich sind und berechne den Gewinn entsprechend
    elif spin1 == spin2 or spin1 == spin3 or spin2 == spin3:
        winnings = amount * 2
        result = f"doppel einsatz {winnings}\n{spin1} {spin2} {spin3}"
    # Wenn keine der obigen Bedingungen erfüllt ist, hat der Benutzer verloren
    else:
        winnings = -amount
        rawwin = abs(winnings)
        result = f"Sorry, you lost {rawwin} chips.\n{spin1} {spin2} {spin3}"
        
    # Füge den Gewinn oder Verlust zu den Münzen des Benutzers hinzu und speichere sie in der JSON-Datei
    coins[user_id] += winnings
    with open(config.data["coinsfile"], 'w') as f:
            json.dump(coins, f)
    
    # Gib das Ergebnis zurück
    return result
