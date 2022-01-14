import json

def insert_config(guild_id, data: dict=None, *, append: bool, key: str=None, value=None):
    with open("config.json") as file:
        decoded = json.load(file)
    
    if append:
        decoded[guild_id][key] = value
    else:
        decoded[guild_id] = data

    with open("config.json", "w") as file:
        json.dump(decoded, file, indent=4)

def get_all_data():
    with open("config.json") as file:
        return json.load(file)