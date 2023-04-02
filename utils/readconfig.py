import json
def readconfig(configfile):
    with open(configfile) as f:
        
        config = json.load(f)
        return config
        
