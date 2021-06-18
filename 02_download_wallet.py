#Import packages
import daltonapi
import time
import os
from datetime import datetime
from daltonapi.api import Atom
import requests

#Start Atom and set object values
atom = Atom()
walletID = "mynima.gm"
date = datetime.today().strftime('%Y-%m-%d')
exclude_list = ["DOKI DOKI PUNKS","Key Moment 4 Creation"]

#Get output folder setup
newpath = f"C:/Users/ipsan/Downloads/{walletID}/{date}"
if not os.path.exists(newpath):
    os.makedirs(newpath)

#Get all the assets for the wallet
assets = atom.get_assets(owner=walletID)

#Go through folder assets and download the images.
for a in assets:
    asset = atom.get_asset(a.key)
    name = asset.name
    image = asset.image
    response = requests.get(image)
    if name not in exclude_list:
        exclude_list.append(str(name))
        file = open(f"{newpath}/{name}.png", "wb")
        file.write(response.content)
        file.close()
        time.sleep(0.4)

print(f"All images have been downloaded from {walletID} to {newpath}. Enjoy!")