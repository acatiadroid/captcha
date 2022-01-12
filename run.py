from decouple import config
from utils.botinstance import Bot

extensions = [
    "cogs.setup",
    "cogs.captcha",
]

bot = Bot()

if __name__ == "__main__":
    for ext in extensions:
        bot.load_extension(ext)
    bot.ipc.start()
    bot.run(config("TOKEN"))
