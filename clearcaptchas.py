# A helpful file for removing all files in the captchas/ folder.

import os

for file in os.listdir("captchas/"):
    os.remove("captchas/" + file)