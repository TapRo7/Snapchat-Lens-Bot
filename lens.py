import discord
from discord.ext import commands, tasks
from discord import app_commands, ui
import os
from src.save_html import save_html
from src.scrape_data import scrape_data
from src.video_downloader import download_video
import asyncio

# Only default intents are needed as this bot's purpose is only to run one application command
intents = discord.Intents.default()

# Client declaration - Rare prefix to prevent accidental calls
bot = commands.Bot(command_prefix='l!', intents=intents)

# General Error handler, also includes a permission check faliure in case that is implemented in the future
@bot.tree.error
async def on_command_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.CheckFailure):
        try:
            await interaction.response.send_message("You don't have permissions to use this command.", ephemeral=True)
        except:
            await interaction.followup.send("You don't have permissions to use this command.", ephemeral=True)
    else:
        try:
            await interaction.response.send_message("An unknown error occurred. Please try again later.", ephemeral=True)
        except:
            await interaction.followup.send("An unknown error occurred. Please try again later.", ephemeral=True)
        
        print(f"Unhandled Error: {error} in app command by {interaction.user} ({interaction.user.id})")

# On ready event, syncing commands, and changing bot's status to Watching Snapchat
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)!")
    except Exception as e:
        print(f"Sync Failed! {e}")

    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Snapchat"))

# Create a lock so that the video or HTML doesn't get overridden in multiple usage cases
command_locker = asyncio.Lock()

# Command to get the lens embed
@bot.tree.command(name="lens", description="Share a Snap Lens Snap code and preview video in the channel!")
@app_commands.guild_only()
@app_commands.describe(url = "Please enter the Snap Lens URL")
async def lens(interaction : discord.Interaction, url : str):
    try:
        await interaction.response.defer(ephemeral=True)
    except:
        print("Interaction Timed Out")

    url = url.lower()

    if not (url.startswith("https://lens.snapchat.com") or url.startswith("https://www.snapchat.com/lens")):
        await interaction.followup.send("The provided URL is not a valid lens URL.\nMake sure the URL contains `https://` at the start, and is of either one of these formats:\n- https://www.snapchat.com/lens/1e0ee80109...\n- https://lens.snapchat.com/1e0ee80109...", ephemeral=True)
        return
    
    async with command_locker:
        html_save_response = save_html(url)
        if not html_save_response:
            await interaction.followup.send("An unknown error occured, please try again later.", ephemeral=True)
            return

        scrape_data_response = scrape_data()
        if scrape_data_response == 1: # Error code for invalid file path - This shouldn't happen as we always save as website.html
            await interaction.followup.send("An unknown error occured, please inform a staff member regarding this.\nError code 1.", ephemeral=True)
            return
        elif not scrape_data_response: # In case an error occurs in the scraping which should not happen under normal circumstances
            await interaction.followup.send("An unknown error occured, please try again later.", ephemeral=True)
            return
        
        image_url = scrape_data_response[0]
        video_url = scrape_data_response[1]
        lens_creator = scrape_data_response[2]
        lens_name = scrape_data_response[3]
        
        video_download_response = download_video(video_url)
        if not video_download_response:
            await interaction.followup.send("An unknown error occured, please try again later.", ephemeral=True)
            return
        
        with open("video.mp4", 'rb') as file:
            video = discord.File(file)

        embed = discord.Embed(
            title = f"{lens_name} created by {lens_creator}",
            colour = discord.Color.from_rgb(255,252,0),
            description=f"[{lens_name} Link]({url})\n\nSnapcode Image 👇"
        )
        embed.set_author(name=f"{interaction.user.name} ({interaction.user.id})", icon_url=interaction.user.avatar)
        embed.set_image(url=image_url)

        await interaction.channel.send(embed=embed, file=video)

    await interaction.followup.send("Your lens has been posted!", ephemeral=True)

# Run the bot
bot.run(os.getenv('Token'))