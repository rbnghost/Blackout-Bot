
import json

def getcoins(configfile):
    with open(configfile, 'r') as f:
        coins = json.load(f)
    return coins
