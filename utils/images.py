from captcha.image import ImageCaptcha
import string
import random
import discord
import os

def generate_captcha(*, chars: int = 5):
    text = ''.join(random.choice(string.digits + string.ascii_lowercase)
                   for _ in range(chars))
    file_name = ''.join(random.choice(string.ascii_uppercase +
                        string.digits + string.ascii_lowercase) for _ in range(25))
    image = ImageCaptcha(width=280, height=90)
    image.write(text, f"captchas/{file_name}.png")

    return {
        "filename": file_name + ".png",
        "file_src": discord.File(f"captchas/{file_name}.png", filename="captcha.png"),
        "text": text.lower(),
        "chars": chars
    }

def delete_captcha(*, filename: str):
    """Don't include .png"""
    try:
        os.remove("captchas/" + filename + ".png")
        return True
    except FileNotFoundError:
        return False
    
