# Snapchat Lens Bot

# Overview
A simple Python Discord Bot that takes a Snapchat lens link as input in a command and outputs an embed with information on the lens, the lens snap code as the embed image, and the lens preview video on the message.

# Setup
- Create a .env file in the same directory as the `lens.py` file and put your discord bot's token inside as following:
  - `Token=YOUR_BOT_TOKEN`
- Run the bot using a process manager such as PM2 on your VPS, the main file to run is `lens.py`


# Usage
- The `/lens` command will appear in the bot's server. It has no restrictions by default but you can set them via the Discord client in Server Settings -> Integrations -> Your Bot -> lens command -> Set Permissions
- People can paste in Snapchat Lens URLs and it will paste their lens video and Lens Code image in an embed in the channnel


# Disk Usage
- The bot automatically wipes the previous HTML and video from the disk so that memory isn't overused. Storage is not an issue.