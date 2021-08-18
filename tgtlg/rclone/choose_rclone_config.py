# This is code to switch which rclone config section to use. This setting affects the entire bot(And at this time, the cloneHelper only support gdrive, so you should only choose to use gdrive config section)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) xiaoqi-beta | gautamajay52

import configparser  # buildin package
import logging
import os
import re

import pyrogram.types as pyrogram
from pyrogram.types import CallbackQuery
from .. import LOGGER, OWNER_ID

config = configparser.ConfigParser()

async def rclone_command_f(client, message):
    """/rclone command"""
    LOGGER.info(f"Recieved Rclone Command. Chat ID: {message.chat.id}, User ID: {message.from_user.id}")
    if message.from_user.id == OWNER_ID and message.chat.type == "private" and os.path.exists("rclone.conf"):
        # make it so that it will check if rclone.conf and rclone_bak.conf exists,
        # and if not, create them
        config.read("rclone_bak.conf")
        sections = list(config.sections())
        inline_keyboard = []
        for section in sections:
            ikeyboard = [
                pyrogram.InlineKeyboardButton(
                    section, callback_data=(f"rclone_{section}").encode("UTF-8")
                )
            ]
            inline_keyboard.append(ikeyboard)
        config.read("rclone.conf")
        section = config.sections()[0]
        msg_text = f"""Default section of rclone config is: **{section}**\n
There are {len(sections)} sections in your rclone.conf file, 
please choose which section you want to use:"""
        ikeyboard = [
            pyrogram.InlineKeyboardButton(
                "Cancel", callback_data=(f"rcloneCancel").encode("UTF-8")
            )
        ]
        inline_keyboard.append(ikeyboard)
        reply_markup = pyrogram.InlineKeyboardMarkup(inline_keyboard)
        await message.reply_text(text=msg_text, reply_markup=reply_markup)
    else:
        await message.reply_text("You have no permission!")
        LOGGER.warning(
            f"UID = {message.from_user.id} has no permission to edit rclone config!"
        )
