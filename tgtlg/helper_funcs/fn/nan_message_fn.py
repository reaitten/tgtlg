import pyrogram
from pyrogram import Client
from tgtlg import app, LOGGER

def nan(client, message):
    LOGGER.info('UID: {} - UN: {} - MSG: {}'.format(message.from_user.id, message.chat.username, message.text))