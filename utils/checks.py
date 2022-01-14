from discord.ext import commands


async def check_guild_permissions(ctx, perms, *, check=all):
    is_owner = await ctx.bot.is_owner(ctx.author)
    if is_owner:
        return True

    if ctx.guild is None:
        return False

def has_elevated_perms():
    async def pred(ctx):
        return await check_guild_permissions(ctx, {"manage_members": True})
    
    return commands.check(pred)

def guild_manager():
    async def pred(ctx):
        return await check_guild_permissions(ctx, {"manage_guild": True})

    return commands.check(pred)