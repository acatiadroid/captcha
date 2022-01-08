import json

def insert_config(data: dict, ctx):
    with open("config.json") as file:
        decoded = json.load(file)
    
    decoded[ctx.guild.id] = data

    with open("config.json", "w") as file:
        json.dump(decoded, file, indent=4)

def get_all_data():
    with open("config.json") as file:
        return json.load(file)