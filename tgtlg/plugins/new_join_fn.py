import logging
import time
import pyrogram

from tgtlg import AUTH_CHANNEL, LOGGER, BOT_START_TIME

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def new_join_f(client, message):
    chat_type = message.chat.type
    if chat_type != "private":
        await message.reply_text(
            f"""<b>Not Authorized to be here.</b>\n\n<b>Current Chat ID: <code>{message.chat.id}</code>""", parse_mode="html")
        # leave chat
        await client.leave_chat(chat_id=message.chat.id, delete=True)
    # delete all other messages, except for AUTH_CHANNEL
    await message.delete(revoke=True)

async def start_message_f(client, message):
    uptime = get_readable_time((time.time() - BOT_START_TIME))
    await message.reply_text(
        f"""Hi, I've been alive for `{uptime}`. \nTo see the list of available commands, do /help.""")

async def help_message_f(client, message):
    # await message.reply_text("no one gonna help you 🤣🤣🤣🤣", quote=True)
    # channel_id = str(AUTH_CHANNEL)[4:]
    # message_id = 99
    # display the /help

    await message.reply_text(
        """Available Commands:
/help: To get this message

/leech: This command should be used as reply to a magnetic link, a torrent link, or a direct link. [this command will SPAM the chat and send the downloads a seperate files, if there is more than one file, in the specified torrent]
/archive: This command should be used as reply to a magnetic link, a torrent link, or a direct link. [This command will create a .tar.gz file of the output directory, and send the files in the chat, splited into PARTS of 1024MiB each, due to Telegram limitations]
/extract: This will unarchive file and upload to telegram.

/gleech: This command should be used as reply to a magnetic link, a torrent link, or a direct link. And this will download the files from the given link or torrent and will upload to the cloud using rclone.
/garchive: This command will compress the folder/file and will upload to your cloud.
/gextract: This will unarchive file and upload to cloud.
/gclone: This command is used to clone gdrive files or folder using gclone.
Syntax: `[ID of the file or folder][one space][name of your folder only (If the ID is of file, don't put anything)]` and then reply /gclone to it.

/tleech: This will mirror the telegram files to your respective cloud.
/textract: This will unarchive telegram file and upload to cloud.

/ytdl: This command should be used as reply to a [supported link](https://ytdl-org.github.io/youtube-dl/supportedsites.html)
/pytdl: This command will download videos from youtube playlist link and will upload to telegram.
/gytdl: This will download and upload to your cloud.
/gpytdl: This download youtube playlist and upload to your cloud.

/getsize: This will give you total size of your destination folder in cloud.
/renewme: This will clear the remains of downloads which are not getting deleted after upload of the file or after /cancel command.
/rename: To rename the telegram files.

/savethumb: Reply to a image to set following files with this thumbnail.
/clearthumb: Clear saved thumbnail.

/rclone: This will change your drive config on fly. (First one will be default)
/log: This will send you a txt file of the logs.

Only works with direct link and youtube link for now.
You can add a custom name as it's prefix to the file. Example: if gk.txt uploaded will be what you add in CUSTOM_FILE_NAME + gk.txt
 
And also added custom name like...
You have to pass link as www.download.me/gk.txt | new.txt 
the file will be uploaded as new.txt.

Get started!
Send any one of the available commands, as a reply to a valid link/magnet/torrent.""",
        disable_web_page_preview=True,
    )

# fr. https://github.com/breakdowns/slam-mirrorbot/blob/551c8b6f690f835547fb430188818767e5cc7c68/bot/helper/ext_utils/bot_utils.py#L123 

def get_readable_time(seconds: int) -> str:
    result = ''
    (days, remainder) = divmod(seconds, 86400)
    days = int(days)
    if days != 0:
        result += f'{days}d'
    (hours, remainder) = divmod(remainder, 3600)
    hours = int(hours)
    if hours != 0:
        result += f'{hours}h'
    (minutes, seconds) = divmod(remainder, 60)
    minutes = int(minutes)
    if minutes != 0:
        result += f'{minutes}m'
    seconds = int(seconds)
    result += f'{seconds}s'
    return result
