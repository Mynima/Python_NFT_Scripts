#Import packages
import daltonapi
import time
import os
from datetime import datetime
from daltonapi.api import Atom
import requests

#Start Atom and set object values
atom = Atom()
walletID = ""       #Add wallet address here
FolderPath = ""     #Add folder pathwat here (note that "/" should be used not "\")
exclude_list = []   #Add comma sparated "" list of any items you don't want to download
gif_list = []       #Add known animated NFTs as comma sparated "" list here
date = datetime.today().strftime('%Y-%m-%d')

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
    #Some handling of animated/gif files, needs to be updated to include more robust methodology
    if asset.name.upper().find("CREATION") > 0 or asset.name.upper().find("ANIMATE") > 0 or asset.image.upper().find(".GIF") > 0 or name in gif_list:
        ext = "gif"
    else:
        ext = "png"
    if name not in exclude_list:
        exclude_list.append(str(name))
        file = open(f"{newpath}/{name}.{ext}", "wb")
        file.write(response.content)
        file.close()
        #Time delay added to help prevent API from failing with too many requests at once. 
        time.sleep(0.4)

print(f"All images have been downloaded from {walletID} to {newpath}. Enjoy!")