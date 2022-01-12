from .botinstance import Bot
from .json_wrapper import insert_config

bot = Bot()

@bot.ipc.route()
async def guild_data(data):
    guild = bot.get_guild(data.guild_id)

    g_data = {
        "name": guild.name,
        "roles": guild.roles,
        "id": guild.id
    }

    return g_data

@bot.ipc.route()
async def frm_post(data):
    insert_config(
        
    )

@bot.ipc.route()
async def all_guilds(data):
    guilds = []
    for guild in bot.guilds:
        guilds.append(guild.id)

    return guilds