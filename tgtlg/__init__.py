#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K | gautamajay52
# modified by reaitten/orsixtyone

import logging
import os
import time
import dotenv
import asyncio

from logging.handlers import RotatingFileHandler
from collections import defaultdict
from sys import exit
from pyrogram import Client
from pyrogram.raw import functions, types
from pyrogram.raw.base import BotCommand

from .bot_utils.bot_cmds import BotCommands

# about cmd to do
__version__ = "1.4.0 - dev"

if os.path.exists("log.txt"):
    with open("log.txt", "r+") as f_d:
        f_d.truncate(0)

# the logging things
logging.basicConfig(
    level=logging.DEBUG, # change to info if you don't want to see the detailed statistics
    format="%(asctime)s - %(levelname)s - %(message)s [%(filename)s:%(lineno)d]",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler(
            "log.txt", maxBytes=50000000, backupCount=10
        ),
        logging.StreamHandler(),
    ],
)
logging.getLogger("pyrogram").setLevel(logging.INFO)
logging.getLogger("urllib3").setLevel(logging.INFO)
logging.getLogger("PIL").setLevel(logging.INFO)

LOGGER = logging.getLogger(__name__)

user_specific_config=dict()

dotenv.load_dotenv("config.env")

# checking compulsory variables
for imp in ["TG_BOT_TOKEN", "APP_ID", "API_HASH", "OWNER_ID", "AUTH_CHANNEL"]:
    try:
        value = os.environ[imp]
        if not value:
            raise KeyError
    except KeyError:
        LOGGER.critical(f"{imp} is missing from enviorment variables and/or config.env.")
        exit()

# The Telegram API things
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")
APP_ID = int(os.environ.get("APP_ID"))
API_HASH = os.environ.get("API_HASH")
OWNER_ID = int(os.environ.get("OWNER_ID"))

# Get these values from my.telegram.org
# to store the channel ID who are authorized to use the bot
AUTH_CHANNEL = [int(x) for x in os.environ.get("AUTH_CHANNEL", "").split()]

# the download location, where the HTTP Server runs
DOWNLOAD_LOCATION = os.environ.get("DOWNLOAD_LOCATION", "./Downloads")

# Telegram maximum file upload size
MAX_FILE_SIZE = int(os.environ.get("MAX_FILE_SIZE", 50000000))
TG_MAX_FILE_SIZE = int(os.environ.get("TG_MAX_FILE_SIZE", 2097152000))
FREE_USER_MAX_FILE_SIZE = int(os.environ.get("FREE_USER_MAX_FILE_SIZE", 50000000))

# adds OWNER_ID to AUTH_CHANNEL, doesn't check if OWNER_ID is already in AUTH_CHANNEL
AUTH_CHANNEL.append(OWNER_ID)

# chunk size that should be used with requests
CHUNK_SIZE = int(os.environ.get("CHUNK_SIZE", 128))

# default thumbnail to be used in the videos
DEF_THUMB_NAIL_VID_S = os.environ.get("DEF_THUMB_NAIL_VID_S", "https://telegra.ph/file/a4bf864c890f7d9016662.jpg")
# maximum message length in Telegram
MAX_MESSAGE_LENGTH = int(os.environ.get("MAX_MESSAGE_LENGTH", 4096))

# set timeout for subprocess
PROCESS_MAX_TIMEOUT = int(os.environ.get("PROCESS_MAX_TIMEOUT", 3600))

# touch if you know what you are doing!
SP_LIT_ALGO_RITH_M = os.environ.get("SP_LIT_ALGO_RITH_M", "hjs")
ARIA_TWO_STARTED_PORT = (os.environ.get("ARIA_TWO_STARTED_PORT", 6800))
EDIT_SLEEP_TIME_OUT = int(os.environ.get("EDIT_SLEEP_TIME_OUT", 15))
MAX_TIME_TO_WAIT_FOR_TORRENTS_TO_START = int(os.environ.get("MAX_TIME_TO_WAIT_FOR_TORRENTS_TO_START", 300))
MAX_TG_SPLIT_FILE_SIZE = int(os.environ.get("MAX_TG_SPLIT_FILE_SIZE", 2097151000))

# add config vars for the display progress
FINISHED_PROGRESS_STR = os.environ.get("FINISHED_PROGRESS_STR", "█")
UN_FINISHED_PROGRESS_STR = os.environ.get("UN_FINISHED_PROGRESS_STR", "░")

# add offensive API
TG_OFFENSIVE_API = os.environ.get("TG_OFFENSIVE_API", None)

CUSTOM_FILE_NAME = os.environ.get("CUSTOM_FILE_NAME", "")
RCLONE_CONFIG = os.environ.get("RCLONE_CONFIG", "")
UPTOBOX_TOKEN = os.environ.get("UPTOBOX_TOKEN", None)
DESTINATION_FOLDER = os.environ.get("DESTINATION_FOLDER", "")
INDEX_LINK = os.environ.get("INDEX_LINK", "")
UPLOAD_AS_DOC = os.environ.get("UPLOAD_AS_DOC", "False")

BOT_START_TIME = time.time()
# dict to control uploading and downloading
gDict = defaultdict(lambda: [])
# user settings dict #ToDo
user_settings = defaultdict(lambda: {})
gid_dict = defaultdict(lambda: [])
_lock = asyncio.Lock()

app = Client(
    ':memory:',
    bot_token=TG_BOT_TOKEN,
    api_id=APP_ID,
    api_hash=API_HASH,
    workers=343,
)

def multi_rclone_init():
    if not os.path.exists("rclone.conf") and RCLONE_CONFIG:  # you never know
        LOGGER.critical("found rclone config in variables, but could not find rclone.conf. Upload rclone.conf to root directory of repo!")
        exit()
    if not os.path.exists("rclone_bak.conf") and os.path.exists("rclone.conf"):  # backup rclone.conf file
        with open("rclone_bak.conf", "w+", newline="\n", encoding="utf-8") as fole:
            with open("rclone.conf", "r") as f:
                fole.write(f.read())
        LOGGER.info("rclone.conf backuped to rclone_bak.conf!")

def bcmds(app):
    tBC = types.BotCommand
    botcmds = [
    tBC(command=f'{BotCommands.StartCommand}', description='Get Start Msg'),
    tBC(command=f'{BotCommands.HelpCommand}', description='Get Detailed Help'),
    tBC(command=f'{BotCommands.LeechCommand}', description='Start Leeching'),
    tBC(command=f'{BotCommands.ArchiveCommand}', description='Archive Leech'),
    tBC(command=f'{BotCommands.ExtractCommand}', description='Extract Leech'),
    tBC(command=f'{BotCommands.RcloneLeechCommand}', description='Leech & Upload to Drive'),
    tBC(command=f'{BotCommands.RcloneLeechArchiveCommand}', description='Leech, Archive, & Upload to Drive'),
    tBC(command=f'{BotCommands.RcloneLeechExtractCommand}', description='Leech, Extract, & Upload to Drive'),
    tBC(command=f'{BotCommands.CloneCommand}', description='Clone GDrive Files'),
    tBC(command=f'{BotCommands.TelegramLeechCommand}', description='Leech Telegram Files & Upload to Drive'),
    tBC(command=f'{BotCommands.TelegramLeechExtractCommand}', description='Leech Telegram Files, Extract, & Upload to Drive'),
    tBC(command=f'{BotCommands.CancelCommand}', description='Cancel Leech'),
    tBC(command=f'{BotCommands.YoutubeDownloaderCommand}', description='Leech YT Videos, & supported Links'),
    tBC(command=f'{BotCommands.PlaylistYoutubeDownloaderCommand}', description='Leech YT Playlists'),
    tBC(command=f'{BotCommands.RcloneYoutubeDownloaderCommand}', description='Leech YT Videos, supported Links, and Upload to Drive'),
    tBC(command=f'{BotCommands.RclonePlaylistYoutubeDownloaderCommand}', description='Leech YT Playlists, and Upload to Drive'),
    tBC(command=f'{BotCommands.StatusCommand}', description='Check Status'),
    tBC(command=f'{BotCommands.SaveThumbnailCommand}', description='Save Image for Thumbnail'),
    tBC(command=f'{BotCommands.ClearThumbnailCommand}', description='Clear Saved Thumbnail'),
    tBC(command=f'{BotCommands.RenameCommand}', description='Rename Telegram Files'),
    tBC(command=f'{BotCommands.ReNewMeCommand}', description='Clear bugged downloads'),
    tBC(command=f'{BotCommands.SearchHelpCommand}', description='Search for Torrents'),
    tBC(command=f'{BotCommands.NyaasiCommand}', description='Search On Nyaa.si'),
    tBC(command=f'{BotCommands.SukebeiCommand}', description='Search On Sukebei (+18)'),
    tBC(command=f'{BotCommands.ToggleVideoCommand}', description='Upload as a Video'),
    tBC(command=f'{BotCommands.ToggleDocumentCommand}', description='Upload as a Document'),
    tBC(command=f'{BotCommands.RcloneConfigCommand}', description='Change rclone Config'),
    tBC(command=f'{BotCommands.GetRcloneSizeCommand}', description='Get Rclone Destination Folder Size'),
    tBC(command=f'{BotCommands.LogCommand}', description='Get Logs')
    ]
    app.send(functions.bots.SetBotCommands(commands=botcmds))
    LOGGER.info("Added Bot CMDS!")

multi_rclone_init()
# start app (weird place right?)
app.start()
# get bot username and set it as a local variable (because don't wanna use ptb)
buname = "@" + app.get_me().username