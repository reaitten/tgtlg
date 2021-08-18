#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K | gautamajay52
# modified by reaitten/orsixtyone

import asyncio
import logging
import os
import re
import sys
import time
import requests
import math

import aria2p
from pyrogram.errors import FloodWait, MessageNotModified
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from tgtlg import (
    ARIA_TWO_STARTED_PORT,
    AUTH_CHANNEL,
    CUSTOM_FILE_NAME,
    DOWNLOAD_LOCATION,
    EDIT_SLEEP_TIME_OUT,
    LOGGER,
    MAX_TIME_TO_WAIT_FOR_TORRENTS_TO_START,
    FINISHED_PROGRESS_STR,
    UN_FINISHED_PROGRESS_STR
)
from ..bot_utils.create_compressed_archive import (create_archive, get_base_name, unzip_me)
from ..bot_utils.conversion import convert_size, convert_to_bytes
from ..helper_funcs.extract_link_from_message import extract_link
from ..helper_funcs.uploader import upload_with_rclone, upload_to_tg

from .exceptions import DirectDownloadLinkException
from .direct_link_generator import direct_link_generator
from .telegram_downloader import download_tg


# unsure what this does
def KopyasizListe(string):
    kopyasiz = list(string.split(","))
    kopyasiz = list(dict.fromkeys(kopyasiz))
    return kopyasiz

# unsure what this does
def Virgullustring(string):
    string = string.replace("\n\n",",")
    string = string.replace("\n",",")
    string = string.replace(",,",",")
    string = string.rstrip(',')
    string = string.lstrip(',')
    return string

tracker_urlsss = [
    "https://raw.githubusercontent.com/XIU2/TrackersListCollection/master/all.txt",
    "https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_all.txt",
    "https://raw.githubusercontent.com/DeSireFire/animeTrackerList/master/AT_all.txt"
    ]
tumtorrenttrackerstringi = ""
sonstringtrckr = ""
for i in range(len(tracker_urlsss)):
    response = requests.get(tracker_urlsss[i])
    response.encoding = "utf-8"
    tumtorrenttrackerstringi += "\n"
    tumtorrenttrackerstringi += response.text
trackerlistemiz = KopyasizListe(Virgullustring(tumtorrenttrackerstringi))
sonstringtrckr = ','.join(trackerlistemiz)
# LOGGER.info(sonstringtrckr)
# trackelreri alıyoz dinamik olarak
async def aria_start():
    global sonstringtrckr
    aria2_daemon_start_cmd = []
    # start the daemon, aria2c command
    aria2_daemon_start_cmd.append("aria2c")
    aria2_daemon_start_cmd.append("--allow-overwrite=true")
    aria2_daemon_start_cmd.append("--daemon=true")
    # aria2_daemon_start_cmd.append(f"--dir={DOWNLOAD_LOCATION}")
    # TODO: this does not work, need to investigate this.
    # but for now, https://t.me/TrollVoiceBot?start=858
    # reaitten note: i have no idea what this voice message says as I do not know this language
    aria2_daemon_start_cmd.append("--enable-rpc")
    aria2_daemon_start_cmd.append("--follow-torrent=mem")
    aria2_daemon_start_cmd.append("--max-connection-per-server=10")
    aria2_daemon_start_cmd.append("--min-split-size=10M")
    aria2_daemon_start_cmd.append("--rpc-listen-all=false")
    aria2_daemon_start_cmd.append(f"--rpc-listen-port={ARIA_TWO_STARTED_PORT}")
    aria2_daemon_start_cmd.append("--rpc-max-request-size=1024M")
    aria2_daemon_start_cmd.append(f"--bt-tracker={sonstringtrckr}")
    aria2_daemon_start_cmd.append("--bt-max-peers=0")
    aria2_daemon_start_cmd.append("--seed-ratio=1.0")
    aria2_daemon_start_cmd.append("--seed-time=0")
    # using qbittorrent user and peer agent
    aria2_daemon_start_cmd.append("--peer-id-prefix=-qB4360-")
    aria2_daemon_start_cmd.append("--user-agent=qBittorrent/4.3.6")
    aria2_daemon_start_cmd.append("--peer-agent=qBittorrent/4.3.6")
    aria2_daemon_start_cmd.append("--max-overall-upload-limit=1K")
    aria2_daemon_start_cmd.append("--split=10")
    aria2_daemon_start_cmd.append(f"--bt-stop-timeout={MAX_TIME_TO_WAIT_FOR_TORRENTS_TO_START}")

    LOGGER.info("Started aria2c process.")
    LOGGER.debug(aria2_daemon_start_cmd)
    process = await asyncio.create_subprocess_exec(
        *aria2_daemon_start_cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()

    aria2 = aria2p.API(
        aria2p.Client(host="http://localhost",
                      port=ARIA_TWO_STARTED_PORT, secret="")
    )
    LOGGER.debug(aria2)
    return aria2

def add_magnet(aria_instance, magnetic_link, c_file_name):
    options = None
    # if c_file_name is not None:
    #     options = {
    #         "dir": c_file_name
    #     }
    try:
        download = aria_instance.add_magnet(magnetic_link, options=options)
    except Exception as e:
        return (
            False,
            "**Failed.** \n" + str(e) + " \n<b>Your torrent is dead.</b>",
        )
    else:
        return True, "" + download.gid + ""


def add_torrent(aria_instance, torrent_file_path):
    if torrent_file_path is None:
        return (
            False,
            "**Failed.** \n"
            + str(e)
            + " \nsomething went wrong when trying to add the <u>torrent</u> file.",
        )
    if os.path.exists(torrent_file_path):
        # Add Torrent Into Queue
        try:
            download = aria_instance.add_torrent(
                torrent_file_path, uris=None, options=None, position=None
            )
        except Exception as e:
            return (
                False,
                "**Failed.** \n"
                + str(e)
                + " \n<b>Your torrent is dead.</b>",
            )
        else:
            return True, "" + download.gid + ""
    else:
        return False, "**Failed.** \nPlease try other sources to get workable link."


def add_url(aria_instance, text_url, c_file_name):
    options = None
    # file selection?
    # if c_file_name is not None:
    #     options = {
    #         "dir": c_file_name
    #     }

    # set uri var before checking link with dirlinkgen.py 
    uris = [text_url]
    # moved to tgtlg/helper_funcs/direct_link_generator.py
    # check link with direct link generator
    try:
        urisitring = direct_link_generator(text_url)
        uris = [urisitring]
    except DirectDownloadLinkException as e:
        if "YouTube" in str(e):
            LOGGER.error(f'{text_url}: Someone tried to leech YouTube link via Leech Commands.')
            return (
                False,
                str(e)
            )
        if "No links found!" or f"No Direct link function found" in str(e):
            LOGGER.info(e)
            pass
        else: 
            LOGGER.error(f'{text_url}: {e}')
            return (
                False,
                "Failed to add the URI to download queue due to:\n\n" + str(e)
            )
    
    # Add URL Into Queue
    try:
        download = aria_instance.add_uris(uris, options=options)
    except Exception as e:
        LOGGER.error(e)
        if uris.startswith("http", "https"): 
            return (
                False,
                "**Failed.** \n" + str(e) + " \nTry again later.",
            )
        else:
            return (
                False,
                f"**Failed**\n" + str(e) + "\nYour link needs to have http:// or https:// in the beginning of the link.",
            )
    else:
        return True, "" + download.gid + ""

async def call_apropriate_function(
    aria_instance,
    incoming_link,
    c_file_name,
    sent_message_to_update_tg_p,
    is_zip,
    cstom_file_name,
    is_cloud,
    is_unzip,
    is_file,    
    user_message,
    client,
):
    if not is_file:
        if incoming_link.lower().startswith("magnet:"):
            sagtus, err_message = add_magnet(
                aria_instance, incoming_link, c_file_name)
        elif incoming_link.lower().endswith(".torrent"):
            sagtus, err_message = add_torrent(aria_instance, incoming_link)
        else:
            sagtus, err_message = add_url(
                aria_instance, incoming_link, c_file_name)
        if not sagtus:
            return sagtus, err_message
        LOGGER.info(err_message)
        # https://stackoverflow.com/a/58213653/4723940
        await check_progress_for_dl(
            aria_instance, err_message, sent_message_to_update_tg_p, None
        )
        if incoming_link.startswith("magnet:"):
            err_message = await check_metadata(aria_instance, err_message)
            await asyncio.sleep(1)
            if err_message is not None:
                await check_progress_for_dl(
                    aria_instance, err_message, sent_message_to_update_tg_p, None
                )
            else:
                return False, "Unable to get metadata. \n\n#MetaDataError"
        await asyncio.sleep(1)
        try:
            file = aria_instance.get_download(err_message)
        except aria2p.client.ClientException as ee:
            LOGGER.error(ee)
            return True, None
        to_upload_file = file.name
        com_g = file.is_complete
    else:
        await sent_message_to_update_tg_p.delete()
        to_upload_file, sent_message_to_update_tg_p = await download_tg(client=client, message=user_message)
        if not to_upload_file:
            return True, None
        com_g = True
    if is_zip:
        check_if_file = await create_archive(to_upload_file)
        if check_if_file is not None:
            to_upload_file = check_if_file
    #
    if is_unzip:
        try:
            check_ifi_file = get_base_name(to_upload_file)
            await unzip_me(to_upload_file)
            if os.path.exists(check_ifi_file):
                to_upload_file = check_ifi_file
        except Exception as ge:
            LOGGER.info(ge)
            LOGGER.info(
                f"Unable to extract {os.path.basename(to_upload_file)}, uploading original file."
            )

    if to_upload_file:
        if CUSTOM_FILE_NAME:
            if os.path.isfile(to_upload_file):
                os.rename(to_upload_file,
                          f"{CUSTOM_FILE_NAME}{to_upload_file}")
                to_upload_file = f"{CUSTOM_FILE_NAME}{to_upload_file}"
            else:
                for root, _, files in os.walk(to_upload_file):
                    LOGGER.info(files)
                    for org in files:
                        p_name = f"{root}/{org}"
                        n_name = f"{root}/{CUSTOM_FILE_NAME}{org}"
                        os.rename(p_name, n_name)
                to_upload_file = to_upload_file

    if cstom_file_name:
        os.rename(to_upload_file, cstom_file_name)
        to_upload_file = cstom_file_name
    #
    response = {}
    user_id = user_message.from_user.id
    if user_message.from_user.username:
        mplink = f"@{user_message.from_user.username}"
    else:
        mplink = f'<a href="tg://user?id={user_message.from_user.id}">{user_message.from_user.first_name}</a>'
    if com_g:
        if is_cloud:
            await upload_with_rclone(
                to_upload_file, sent_message_to_update_tg_p, user_message, user_id, mplink
            )
        else:
            final_response = await upload_to_tg(
                sent_message_to_update_tg_p, to_upload_file, user_id, response, client, mplink
            )
            if not final_response:
                return True, None
            try:
                message_to_send = ""
                for key_f_res_se in final_response:
                    local_file_name = key_f_res_se
                    message_id = final_response[key_f_res_se]
                    channel_id = str(sent_message_to_update_tg_p.chat.id)[4:]
                    private_link = f"https://t.me/c/{channel_id}/{message_id}"
                    message_to_send += "✘ <a href='"
                    message_to_send += private_link
                    message_to_send += "'>"
                    message_to_send += local_file_name
                    message_to_send += "</a>"
                    message_to_send += "\n"
                if message_to_send != "":
                    mention_req_user = (
                        f"<b>{mplink}:\nYour requested files:</b>\n\n"
                    )
                    message_to_send = mention_req_user + message_to_send
                    message_to_send = message_to_send + "\n" + "<b>Enjoy!</b>"
                else:
                    message_to_send = "<b>Failed</b> to upload files."
                await user_message.reply_text(
                    text=message_to_send, quote=True, disable_web_page_preview=True
                )
            except Exception as go:
                LOGGER.error(go)
    return True, None

# https://github.com/jaskaranSM/UniBorg/blob/6d35cf452bce1204613929d4da7530058785b6b1/stdplugins/aria.py#L136-L164

# todo- so much unwanted code, I will remove in future after some testing
async def check_progress_for_dl(aria2, gid, event, previous_message):
    while True:
        try:
            file = aria2.get_download(gid)
            complete = file.is_complete
            is_file = file.seeder
            if not complete:
                if not file.error_message:
                    if file.has_failed:
                        # https://pastebin.com/raw/Y5SYsZfn
                        # same reason :facepalm:
                        LOGGER.info(f"Cancelling GID {gid}; failed to retrieve torrent metadata.")
                        await event.reply(f"Download cancelled due to: <i>failed to retrieve torrent metadata.</i>\n\n #MetaDataError", quote=True)
                        file.remove(force=True, files=True)
                        return
                else:
                    msg = file.error_message
                    LOGGER.info(msg)
                    await asyncio.sleep(EDIT_SLEEP_TIME_OUT)
                    await event.reply(f"`{msg}`")
                    return
                await asyncio.sleep(EDIT_SLEEP_TIME_OUT)
                # await check_progress_for_dl(aria2, gid, event, previous_message)
            else:
                LOGGER.info(
                    f"Downloaded Successfully: {file.name} ({file.total_length_string()})"
                )
                # await asyncio.sleep(EDIT_SLEEP_TIME_OUT)
                if not file.is_metadata:
                    await event.edit(
                        f"Downloaded Successfully: `{file.name} ({file.total_length_string()})`"
                    )
                return
        except aria2p.client.ClientException as a2pe:
            await event.reply(
                f"Exception Occured:\n{a2pe}\n<code>{file.name} ({file.total_length_string()})</code>", quote=True
            )
            return
        except MessageNotModified as ep:
            LOGGER.info(ep)
            await asyncio.sleep(EDIT_SLEEP_TIME_OUT)
            # await check_progress_for_dl(aria2, gid, event, previous_message)
            return
        except FloodWait as e:
            LOGGER.info(e)
            time.sleep(e.x)
        except Exception as e:
            LOGGER.info(str(e))
            if "not found" in str(e) or "'file'" in str(e):
                await event.edit(
                    f"Download cancelled:\n<code>{file.name} ({file.total_length_string()})</code>"
                )
                return
            else:
                LOGGER.info(str(e))
                await event.edit(
                    "<u>Error:</u>\n<code>{}</code> \n\n#error".format(str(e))
                )
                return

# https://github.com/jaskaranSM/UniBorg/blob/6d35cf452bce1204613929d4da7530058785b6b1/stdplugins/aria.py#L136-L164


async def check_metadata(aria2, gid):
    file = aria2.get_download(gid)
    if not file.followed_by_ids:
        # https://t.me/c/1213160642/496
        return None
    new_gid = file.followed_by_ids[0]
    LOGGER.info("Changing GID " + gid + " to " + new_gid)
    return new_gid
