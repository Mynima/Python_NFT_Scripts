# 01_get_it_bot.py

#Import libraries
import os
import discord
import random
import daltonapi
import time
import asyncio

#Get specific items from libraries
from discord.ext import commands
from daltonapi.api import Atom
from dotenv import load_dotenv

# Set up using Discord Token and Bot prefix
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix="!")
client = discord.Client()
atom = Atom()


@bot.command(name="asset")
async def on_message(message):
    await message.author.create_dm()
    channeldm = message.author.dm_channel
    channel = message.channel
    await channeldm.send(f'{message.author}, please enter a WAX address.')
    address = ""
    try:
        address = await bot.wait_for("message", timeout=15.0)
        address = address.content
    except asyncio.TimeoutError:
        await channeldm.send("Timed out....")
        return

    if address != "":
        details = []
        await channel.send('Selecting a random asset from the chosen address.')
        assets = atom.get_assets(owner=address)
        tot_asset = len(assets)
        randnum = random.randint(0, tot_asset)
        asset_sel = assets[int(randnum)]
        asset_image = asset_sel.image

        #Get details
        # wallet_address = address
        mint_num = asset_sel.mint[0]
        mint_minted = asset_sel.mint[1]
        mint_max = asset_sel.mint[2]
        if int(mint_max) == 0 and int(mint_minted) > 0:
            mint_max = "Unknown"
        name = asset_sel.name

        schema = asset_sel.schema.key

        #List item details placing them in an array, which is cleared first.
        details.clear()
        # details.append(f"Wallet    : {wallet_address}")   #Address
        details.append(f"**Asset name:** {name}")             #Name
        details.append(f"**Collection:** {collection}")       #Collection
        details.append(f"**Schema:** {schema}")           #Schema
        details.append(f"**Mint** #{mint_num} **of** {mint_minted} (**Max Supply:** {mint_max})") #Mint Number
        
        await channel.send(details[0])
        await channel.send(details[1])
        await channel.send(details[2])
        await channel.send(details[3])
        await channel.send(asset_image)
bot.run(TOKEN)