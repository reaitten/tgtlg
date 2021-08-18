# (c) gautamajay52
#


import asyncio
import os
import shutil
import subprocess

import requests
from ... import DOWNLOAD_LOCATION, LOGGER
from ...helper_funcs.uploader import upload_with_rclone, upload_to_tg


async def yt_playlist_downg(message, i_m_sefg, client, G_DRIVE):
    url = None
    if message.from_user.username:
        mplink = f"@{message.from_user.username}"
    else:
        mplink = f'<a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>'
    if message.reply_to_message:
        url = message.reply_to_message.text
    else:
        url = message.text.split()[1]
    usr = message.message_id
    messa_ge = i_m_sefg.reply_to_message
    fol_der = f"{usr}youtube"
    try:
        os.mkdir(fol_der)
    except:
        pass
    cmd = [
        "youtube-dl",
        "-i",
        "-f",
        "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4",
        "-o",
        f"{fol_der}/%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s",
        f"{url}",
    ]
    gau_tam = await asyncio.create_subprocess_exec(
        *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    gau, tam = await gau_tam.communicate()
    LOGGER.info(gau.decode("utf-8"))
    LOGGER.info(tam.decode("utf-8"))
    e_response = tam.decode().strip()
    ad_string_to_replace = "`please report this issue on https://yt-dl.org/bug . Make sure you are using the latest version; see  https://yt-dl.org/update  on how to update. Be sure to call youtube-dl with the --verbose flag and include its complete output`."
    if e_response and ad_string_to_replace in e_response:
        error_message = e_response.replace(ad_string_to_replace, "")
        await i_m_sefg.edit_text(error_message)
        return False, None
    if G_DRIVE:
        get_g = os.listdir(fol_der)
        for ga_u in get_g:
            ta_m = os.path.join(fol_der, ga_u)
            await upload_with_rclone(ta_m, i_m_sefg, message, usr, mplink)
    else:
        final_response = await upload_to_tg(i_m_sefg, fol_der, usr, {}, client, mplink)
    try:
        shutil.rmtree(fol_der)
    except:
        pass
