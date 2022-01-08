from decouple import config
from utils.botinstance import Bot

extensions = [
    "cogs.setup",
    "cogs.captcha",
]

bot = Bot()

if __name__ == "__main__":
    for ext in extensions:
        Bot().load_extension(ext)
    Bot().run(config("TOKEN"))
