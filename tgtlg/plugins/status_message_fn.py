#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K | gautamajay52
# modified by reaitten/orsixtyone

import asyncio
import io
import logging
import os
import shutil
import sys
import time
import traceback

from tgtlg import AUTH_CHANNEL, BOT_START_TIME, LOGGER, MAX_MESSAGE_LENGTH, user_specific_config
from tgtlg.helper_funcs.admin_check import AdminCheck

# the logging things
from tgtlg.helper_funcs.display_progress import TimeFormatter, humanbytes
from tgtlg.helper_funcs.download_aria_p_n import aria_start, call_apropriate_function
from tgtlg.helper_funcs.upload_to_tg import upload_to_tg
from tgtlg.UserDynaConfig import UserDynaConfig


async def upload_as_doc(client, message):
    user_specific_config[message.from_user.id]=UserDynaConfig(message.from_user.id,True)
    await message.reply_text("**🗞 Your Files Will Be Uploaded As Document 📁**")


async def upload_as_video(client, message):
    user_specific_config[message.from_user.id]=UserDynaConfig(message.from_user.id,False)
    await message.reply_text("**🗞 Your Files Will Be Uploaded As Streamable 🎞**")
    
    
async def status_message_f(client, message):
    aria_i_p = await aria_start()
    # Show All Downloads
    downloads = aria_i_p.get_downloads()
    #
    DOWNLOAD_ICON = "📥"
    UPLOAD_ICON = "📤"
    #
    msg = ""
    for download in downloads:
        downloading_dir_name = "NA"
        try:
            downloading_dir_name = str(download.name)
        except:
            pass
        if download.status == "active":
            total_length_size = str(download.total_length_string())
            progress_percent_string = str(download.progress_string())
            down_speed_string = str(download.download_speed_string())
            up_speed_string = str(download.upload_speed_string())
            download_current_status = str(download.status)
            e_t_a = str(download.eta_string())
            current_gid = str(download.gid)
            #
            msg += f"<u>{downloading_dir_name}</u>"
            msg += " | "
            msg += f"{total_length_size}"
            msg += " | "
            msg += f"{progress_percent_string}"
            msg += " | "
            msg += f"{DOWNLOAD_ICON} {down_speed_string}"
            msg += " | "
            msg += f"{UPLOAD_ICON} {up_speed_string}"
            msg += " | "
            msg += f"{e_t_a}"
            msg += " | "
            msg += f"{download_current_status}"
            msg += " | "
            msg += f"<code>/cancel {current_gid}</code>"
            msg += " | "
            msg += "\n\n"
        # LOGGER.info(msg)

        if msg == "":
            msg = "🤷‍♂️ No Active, Queued or Paused TORRENTs"

    hr, mi, se = up_time(time.time() - BOT_START_TIME)
    total, used, free = shutil.disk_usage(".")
    total = humanbytes(total)
    used = humanbytes(used)
    free = humanbytes(free)

    ms_g = (
        f"<b>Bot Uptime</b>: <code>{hr}h{mi}min{se}sec</code>\n"
        f"<b>Total disk space</b>: <code>{total}</code>\n"
        f"<b>Used</b>: <code>{used}</code>\n"
        f"<b>Free</b>: <code>{free}</code>\n"
    )
    # LOGGER.info(ms_g)

    msg = ms_g + "\n" + msg
    LOGGER.info(msg)
    if len(msg) > MAX_MESSAGE_LENGTH:
        with io.BytesIO(str.encode(msg)) as out_file:
            out_file.name = "status.text"
            await client.send_document(
                chat_id=message.chat.id,
                document=out_file,
            )
    else:
        await message.reply_text(msg, quote=True)


async def cancel_message_f(client, message):
    if len(message.command) > 1:
        # /cancel command
        i_m_s_e_g = await message.reply_text("checking..?", quote=True)
        aria_i_p = await aria_start()
        g_id = message.command[1].strip()
        LOGGER.info(g_id)
        try:
            downloads = aria_i_p.get_download(g_id)
            LOGGER.info(downloads)
            LOGGER.info(downloads.remove(force=True, files=True))
            await i_m_s_e_g.edit_text("Leech Cancelled")
        except Exception as e:
            await i_m_s_e_g.edit_text("<b>Failed.</b>\n\n" + str(e) + "\nAn error occured.")
    else:
        await message.delete()


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
    if message.from_user.id in AUTH_CHANNEL:
        if " " in message.text:
            recvd_command, local_file_name = message.text.split(" ", 1)
            recvd_response = await upload_to_tg(
                imsegd, local_file_name, message.from_user.id, {}, client
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
        await message.reply_document("logs.txt")
