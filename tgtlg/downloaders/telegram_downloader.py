#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) gautamajay52 | Shrimadhav U K
 
import asyncio
import logging
import math
import os
import re
import subprocess
import time

from datetime import datetime
from pathlib import Path
 
from pyrogram import Client, filters
from .. import DOWNLOAD_LOCATION, LOGGER
from ..bot_utils.bot_cmds import BotCommands
from ..bot_utils.create_compressed_archive import unzip_me, get_base_name
from ..status.display_progress import Progress
from ..helper_funcs.uploader import upload_with_rclone
 
 
async def down_load_media_f(client, message):  # to be removed
    user_command = message.command[0]
    user_id = message.from_user.id
    if message.from_user.username:
        mplink = f"@{message.from_user.username}"
    else:
        mplink = f'<a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>'
    #mess_age = await message.reply_text("Waiting..", quote=True)
    if message.reply_to_message is not None:
        the_real_download_location, mess_age = await download_tg(client, message)
        the_real_download_location_g = the_real_download_location
        if user_command == BotCommands.TelegramLeechExtractCommand.lower():
            try:
                check_ifi_file = get_base_name(the_real_download_location)
                file_up = await unzip_me(the_real_download_location)
                if os.path.exists(check_ifi_file):
                    the_real_download_location_g = file_up
            except Exception as ge:
                LOGGER.info(ge)
                LOGGER.info(
                    f"Can't extract {os.path.basename(the_real_download_location)}, Uploading the same file.."
                )
        await upload_with_rclone(the_real_download_location_g, mess_age, message, user_id, mplink)
    else:
        await message.reply_text("Reply to a Telegram Media, to upload to the Cloud Drive.", quote=True)


async def download_tg(client, message):
    user_id = message.from_user.id
    mess_age = await message.reply_text("**Downloading...**", quote=True)
    if not os.path.isdir(DOWNLOAD_LOCATION):
        os.makedirs(DOWNLOAD_LOCATION)
    rep_mess = message.reply_to_message
    if rep_mess is not None:
        file = [rep_mess.document, rep_mess.video, rep_mess.audio]
        file_name = [fi for fi in file if fi is not None][0].file_name
        start_t = datetime.now()
        download_location = str(Path("./").resolve()) + "/"
        c_time = time.time()
        prog = Progress(user_id, client, mess_age)
        try:
            the_real_download_location = await client.download_media(
                message=message.reply_to_message,
                file_name=download_location,
                progress=prog.progress_for_pyrogram,
                progress_args=(file_name, c_time),
            )
        except Exception as g_e:
            await mess_age.edit(str(g_e))
            LOGGER.error(g_e)
            return
        end_t = datetime.now()
        ms = (end_t - start_t).seconds
        LOGGER.debug(f"Real Filepath: {the_real_download_location}")
        await asyncio.sleep(2)
        if the_real_download_location:
            await mess_age.edit_text(
                f"Downloaded Successfully:\nFilename: {file_name}.\nTo Path: <code>{the_real_download_location}</code>.\nTime Taken: <u>{ms}</u> seconds."
            )
        else:
            await mess_age.edit_text(f"Download cancelled or an error occured. Path to document: {the_real_download_location}")
            return None, mess_age
    return the_real_download_location, mess_age
