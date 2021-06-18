#Import packages
import daltonapi
import time
import os
from datetime import datetime
from daltonapi.api import Atom
import requests

#Start Atom and set object values
atom = Atom()
walletID = ""
FolderPath = ""
date = datetime.today().strftime('%Y-%m-%d')
exclude_list = []

#Get output folder setup
newpath = f"{FolderPath}{walletID}/{date}"
if not os.path.exists(newpath):
    os.makedirs(newpath)

#Get all the assets for the wallet
assets = atom.get_assets(owner=walletID)

#Go through assets and download the images to folder.
for a in assets:
    asset = atom.get_asset(a.key)
    name = asset.name
    image = asset.image
    response = requests.get(image)
    if asset.name.upper().find("CREATION") > 0 or asset.name.upper().find("ANIMATE") > 0 or asset.image.upper().find(".GIF") > 0:
        ext = "gif"
    else:
        ext = "png"
    print(name)
    print(image)
    print(ext)
    if name not in exclude_list:
        exclude_list.append(str(name))
        file = open(f"{newpath}/{name}.{ext}", "wb")
        file.write(response.content)
        file.close()
        time.sleep(0.4)

print(f"All images have been downloaded from {walletID} to {newpath}. Enjoy!")