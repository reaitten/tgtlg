#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K | gautamajay52
# modified by reaitten/orsixtyone

import asyncio
import io
import logging
import os
import re
import shutil
import sys
import time
import traceback
import math
import psutil

from ... import (
    AUTH_CHANNEL, 
    BOT_START_TIME, 
    LOGGER, 
    MAX_MESSAGE_LENGTH, 
    user_specific_config, 
    gid_dict, 
    EDIT_SLEEP_TIME_OUT,
    FINISHED_PROGRESS_STR,
    UN_FINISHED_PROGRESS_STR,
    _lock,
)
from ...helper_funcs.admin_check import AdminCheck

# the logging things
from ...status.display_progress import TimeFormatter, humanbytes
from ...downloaders.download_aria_p_n import aria_start, call_apropriate_function
from ...helper_funcs.uploader import upload_to_tg
from ...bot_utils.conversion import convert_size, convert_to_bytes
from ...UserDynaConfig import UserDynaConfig
from ...bot_utils.bot_cmds import BotCommands
from pyrogram.errors import FloodWait, MessageNotModified, MessageIdInvalid

async def upload_as_doc(client, message):
    user_specific_config[message.from_user.id]=UserDynaConfig(message.from_user.id,True)
    await message.reply_text("**Your files will be uploaded as Document.**")


async def upload_as_video(client, message):
    user_specific_config[message.from_user.id]=UserDynaConfig(message.from_user.id,False)
    await message.reply_text("**Your files will be uploaded as Streamable.**")
    
    
async def status_message_f(client, message):  # weird code but 'This is the way' @gautamajay52
    aria_i_p = await aria_start()
    # Show All Downloads
    to_edit = await message.reply("<b>Loading...</b>", quote=True)
    chat_id = int(message.chat.id)
    mess_id = int(to_edit.message_id)
    async with _lock:
        if len(gid_dict[chat_id]) == 0:
            gid_dict[chat_id].append(mess_id)
        else:
            if not mess_id in gid_dict[chat_id]:
                await client.delete_messages(chat_id, gid_dict[chat_id])
                gid_dict[chat_id].pop()
                gid_dict[chat_id].append(mess_id)

    prev_mess = "None"
    #await message.delete()
    while True:
        downloads = aria_i_p.get_downloads()
        msg = ""
        for file in downloads:
            downloading_dir_name = "N/A"
            try:
                downloading_dir_name = str(file.name)
            except:
                pass
            if file.status == "active":
                is_file = file.seeder
                if is_file is None:
                    msgg = f"<b>Connections: {file.connections}</b>"
                else:
                    msgg = f"<b>Seeders:</b> {file.num_seeders} | <b>Peers:</b> {file.connections}"

                dnld_complete = convert_size(round(convert_to_bytes(file.total_length_string()) * (float(re.sub("[^0-9.]", "", file.progress_string()))/100),2))
                percentage = int(file.progress_string(0).split('%')[0])
                prog = "[{0}{1}]".format("".join([FINISHED_PROGRESS_STR for i in range(math.floor(percentage / 5))]),"".join([UN_FINISHED_PROGRESS_STR for i in range(20 - math.floor(percentage / 5))]))

                msg += f"\n<b>Filename:</b> <code>{downloading_dir_name}</code>\n"
                msg += f"\n<b>{prog}</b> <code>{file.progress_string()}</code>"
                msg += f"\n<b>Downloaded</b>: <code>{dnld_complete} of {file.total_length_string()}</code>"
                msg += f"\n<b>Speed</b>: {file.download_speed_string()}"
                msg += f"\n<b>ETA:</b> {file.eta_string()}"
                msg += f"\n{msgg}"
                msg += f"\n<b>GID:</b> <code>{file.gid}</code>\n"

            # tried, just ends up with duplicated 'completed' downloads
            # maybe need time to wait then remove "file.status == complete"
            # but idk about the duplicated part
            # if file.status == "complete":
            #    msg += f"<b>Filename:</b> <code>{downloading_dir_name}</code>"
            #    msg += f"\nDownloaded Sucessfully.\nWaiting for Upload Queue.\n"

        hr, mi, se = up_time(time.time() - BOT_START_TIME)
        total, used, free = shutil.disk_usage(".")
        ram = psutil.virtual_memory().percent
        cpu = psutil.cpu_percent()
        total = humanbytes(total)
        used = humanbytes(used)
        free = humanbytes(free)

        ms_g = (
            f"<b>Bot Uptime</b>: <code>{hr}h{mi}min{se}sec</code>\n"
            f"<b>Total disk space</b>: <code>{total}</code>\n"
            f"<b>Used</b>: <code>{used}</code>\n"
            f"<b>Free</b>: <code>{free}</code>\n"
            f"<b><b>CPU:</b> <code>{cpu}%</code> | RAM:</b> <code>{ram}%</code> \n"
        )
        if msg == "":
            stmsg = "No Active, Queued or Paused Torrents."
            msg = ms_g + "\n" + stmsg
            await to_edit.edit(msg)
            break
        msg = msg + "\n" + ms_g
        if len(msg) > MAX_MESSAGE_LENGTH:  # todo - will catch later
            with io.BytesIO(str.encode(msg)) as out_file:
                out_file.name = "status.text"
                await client.send_document(
                    chat_id=message.chat.id,
                    document=out_file,
                )
            break
        else:
            if msg != prev_mess:
                try:
                    await to_edit.edit(msg, parse_mode="html")
                except MessageIdInvalid as df:
                    break
                except MessageNotModified as ep:
                    LOGGER.info(ep)
                    await asyncio.sleep(EDIT_SLEEP_TIME_OUT)
                except FloodWait as e:
                    LOGGER.info(e)
                    time.sleep(e.x)
                await asyncio.sleep(EDIT_SLEEP_TIME_OUT)
                prev_mess = msg


async def cancel_message_f(client, message):
    i_m_s_e_g = await message.reply_text("Checking..", quote=True)
    if len(message.command) > 1:
        # /cancel command
        aria_i_p = await aria_start()
        g_id = message.command[1].strip()
        LOGGER.info(g_id)
        try:
            tdownloads = aria_i_p.get_download(g_id)
            name = tdownloads.name
            size = tdownloads.total_length_string()
            gid_list = tdownloads.followed_by_ids
            downloads = [tdownloads]
            #if len(gid_list) != 0:
            #    downloads = aria_i_p.get_downloads(gid_list)
            await i_m_s_e_g.edit_text(f"Download cancelled:\n<code>{name} ({size})</code> by <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>")
            # fix fuckup in downloads
            # https://pastebin.com/raw/Y5SYsZfn
            aria_i_p.remove(downloads=downloads, force=True, files=True, clean=True)
        except Exception as e:
            await i_m_s_e_g.edit_text("<b>Failed.</b>\n\n" + str(e) + "\nAn error occured.")
    else:
        await i_m_s_e_g.edit_text(f"You have to enter a <code>GID</code> along with /{BotCommands.CancelCommand} in order to cancel a download.\nUsage: /{BotCommands.CancelCommand} <code>GID</code>")
        #await message.delete()


async def exec_message_f(client, message):
    if message.from_user.id in AUTH_CHANNEL:
        DELAY_BETWEEN_EDITS = 0.3
        PROCESS_RUN_TIME = 100
        cmd = message.text.split(" ", maxsplit=1)[1]

        reply_to_id = message.message_id
        if message.reply_to_message:
            reply_to_id = message.reply_to_message.message_id

        start_time = time.time() + PROCESS_RUN_TIME
        process = await asyncio.create_subprocess_shell(
            cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        e = stderr.decode()
        if not e:
            e = "No Error"
        o = stdout.decode()
        if not o:
            o = "No Output"
        else:
            _o = o.split("\n")
            o = "`\n".join(_o)
        OUTPUT = f"**Query:**\n__Command:__\n`{cmd}` \n__PID:__\n`{process.pid}`\n\n**stderr:** \n`{e}`\n**Output:**\n{o}"

        if len(OUTPUT) > MAX_MESSAGE_LENGTH:
            with io.BytesIO(str.encode(OUTPUT)) as out_file:
                out_file.name = "exec.text"
                await client.send_document(
                    chat_id=message.chat.id,
                    document=out_file,
                    caption=cmd,
                    disable_notification=True,
                    reply_to_message_id=reply_to_id,
                )
            await message.delete()
        else:
            await message.reply_text(OUTPUT)


async def upload_document_f(client, message):
    imsegd = await message.reply_text("Processing ...")
    if message.from_user.username:
        mplink = f"@{message.from_user.username}"
    else:
        mplink = f'<a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>'
    if message.from_user.id in AUTH_CHANNEL:
        if " " in message.text:
            recvd_command, local_file_name = message.text.split(" ", 1)
            recvd_response = await upload_to_tg(
                imsegd, local_file_name, message.from_user.id, {}, client, mplink
            )
            LOGGER.info(recvd_response)
    await imsegd.delete()


async def eval_message_f(client, message):
    if message.from_user.id in AUTH_CHANNEL:
        status_message = await message.reply_text("Processing ...")
        cmd = message.text.split(" ", maxsplit=1)[1]

        reply_to_id = message.message_id
        if message.reply_to_message:
            reply_to_id = message.reply_to_message.message_id

        old_stderr = sys.stderr
        old_stdout = sys.stdout
        redirected_output = sys.stdout = io.StringIO()
        redirected_error = sys.stderr = io.StringIO()
        stdout, stderr, exc = None, None, None

        try:
            await aexec(cmd, client, message)
        except Exception:
            exc = traceback.format_exc()

        stdout = redirected_output.getvalue()
        stderr = redirected_error.getvalue()
        sys.stdout = old_stdout
        sys.stderr = old_stderr

        evaluation = ""
        if exc:
            evaluation = exc
        elif stderr:
            evaluation = stderr
        elif stdout:
            evaluation = stdout
        else:
            evaluation = "Success"

        final_output = (
            "<b>Eval</b>: <code>{}</code>\n\n<b>Output</b>:\n<code>{}</code> \n".format(
                cmd, evaluation.strip()
            )
        )

        if len(final_output) > MAX_MESSAGE_LENGTH:
            with open("eval.text", "w+", encoding="utf8") as out_file:
                out_file.write(str(final_output))
            await message.reply_document(
                document="eval.text",
                caption=cmd,
                disable_notification=True,
                reply_to_message_id=reply_to_id,
            )
            os.remove("eval.text")
            await status_message.delete()
        else:
            await status_message.edit(final_output)


async def aexec(code, client, message):
    exec(
        f"async def __aexec(client, message): "
        + "".join(f"\n {l}" for l in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)


def up_time(time_taken):
    hours, _hour = divmod(time_taken, 3600)
    minutes, seconds = divmod(_hour, 60)
    return round(hours), round(minutes), round(seconds)


async def upload_log_file(client, message):
    g = await AdminCheck(client, message.chat.id, message.from_user.id)
    if g:
        await message.reply_document("log.txt", quote=True)