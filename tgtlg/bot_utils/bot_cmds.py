# Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
# https://github.com/breakdowns/slam-mirrorbot/blob/master/bot/helper/telegram_helper/bot_commands.py
# I do not own anything in this file, they are respecfully owned by https://github.com/lzzy12 and https://github.com/breakdowns. 
# Modified by reaitten/orsixtyone
import os

def getCommand(name: str, command: str):
    try:
        if len(os.environ[name]) == 0:
            raise KeyError
        return os.environ[name]
    except KeyError:
        return command
class _BotCommands:
    def __init__(self):
        self.StartCommand = getCommand('START_COMMAND', 'start')
        self.LeechCommand = getCommand('LEECH_COMMAND', 'leech')
        self.ExtractCommand = getCommand('LEECH_UNZIP_COMMAND', 'extract')
        self.ArchiveCommand = getCommand('LEECH_ZIP_COMMAND', 'archive')
        self.RcloneLeechCommand = getCommand('GLEECH_COMMAND', 'gleech')
        self.RcloneLeechArchiveCommand = getCommand('GLEECH_ZIP_COMMAND', 'garchive')
        self.RcloneLeechExtractCommand = getCommand('GLEECH_UNZIP_COMMAND', 'gextract')
        self.CloneCommand = getCommand('CLONE_COMMAND_G', 'gclone')
        self.TelegramLeechCommand = getCommand('TELEGRAM_LEECH_COMMAND', 'tleech')
        self.TelegramLeechExtractCommand = getCommand('TELEGRAM_LEECH_UNZIP_COMMAND', 'textract')
        self.CancelCommand = getCommand('CANCEL_COMMAND_G', 'cancel')
        self.YoutubeDownloaderCommand = getCommand('YTDL_COMMAND', 'ytdl')
        self.RcloneYoutubeDownloaderCommand = getCommand('GYTDL_COMMAND', 'gytdl')
        self.PlaylistYoutubeDownloaderCommand = getCommand('PYTDL_COMMAND', 'pytdl')
        self.RclonePlaylistYoutubeDownloaderCommand = getCommand('GPYTDL_COMMAND', 'gpytdl')
        self.ToggleVideoCommand = getCommand('TOGGLE_VID', 'togglevid')
        self.ToggleDocumentCommand = getCommand('TOGGLE_DOC', 'toggledoc')
        self.GetRcloneSizeCommand = getCommand('GET_SIZE_G', 'getsize')
        self.RcloneConfigCommand = getCommand('RCLONE_CONFIG_COMMAND', 'rclone')
        self.HelpCommand = getCommand('HELP_COMMAND', 'help')
        self.StatusCommand = getCommand('STATUS_COMMAND', 'status')
        self.LogCommand = getCommand('LOG_COMMAND', 'log')
        self.SaveThumbnailCommand = getCommand('SAVE_THUMBNAIL', 'savethumb')
        self.ClearThumbnailCommand = getCommand('CLEAR_THUMBNAIL', 'clearthumb')
        self.UploadCommand = getCommand('UPLOAD_COMMAND', 'upload')
        self.RenameCommand = getCommand('RENAME_COMMAND', 'rename')
        self.ReNewMeCommand = getCommand('RENEWME_COMMAND', 'renewme')
        self.PurgeCommand = getCommand('PURGE_COMMAND', 'purge')
        self.ExecuteCommand = getCommand('EXEC_COMMAND', 'exec')
        self.EvaluateCommand = getCommand('EVAL_COMMAND', 'eval')
        self.SearchHelpCommand = getCommand('SEARCHHELP_COMMAND', 'searchhelp')
        self.NyaasiCommand = getCommand('NYAASI_COMMAND', 'nyaasi')
        self.SukebeiCommand = getCommand('SUKEBEI_COMMAND', 'sukebei')


BotCommands = _BotCommands()
