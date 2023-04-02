import json

# Importiere die Konfigurationsdaten aus dem Modul "utils.config" und weise sie der Variablen "config" zu
import utils.config as config


def addcoins(user_id, amount):
    
    # Lade die JSON-Daten aus der Datei, die in der Konfigurationsdatei angegeben ist
    with open(config.data["coinsfile"], 'r') as f:
        coins = json.load(f)

    # Wirft eine Ausnahme, falls der Betrag negativ ist
    if amount < 0:
        raise
    
    else:
        coins[user_id] += amount
        # Aktualisiere das Guthaben
        with open(config.data["coinsfile"], 'w') as f:
            json.dump(coins, f)
    
    
def remcoins(user_id, amount):
    
    # Lade die JSON-Daten aus der Datei, die in der Konfigurationsdatei angegeben ist
    with open(config.data["coinsfile"], 'r') as f:
        coins = json.load(f)
        
    # Wirft eine Ausnahme, falls der Betrag negativ ist
    if amount < 0:
        raise
    # Setzt das Guthaben auf 0, falls der Betrag größer ist als das aktuelle Guthaben
    elif amount > coins[user_id]:
        coins[user_id] = 0
        # Aktualisiere das Guthaben
        with open(config.data["coinsfile"], 'w') as f:
            json.dump(coins, f)
    else:
        coins[user_id] -= amount
        # Aktualisiere das Guthaben
        with open(config.data["coinsfile"], 'w') as f:
            json.dump(coins, f)
