  # Telegram Torrent Leecher
  
  A Telegram Torrent (and youtube-dl) Leecher based on [Pyrogram](https://github.com/pyrogram/pyrogram)
  
  # Notice
  Please note that you may face an account ban from Heroku when you deploy this branch on Heroku.
  
  # Table of Contents
  
- [Benefits](#benefits)
- [To-Do](#to-do)
  * [Deployment](#deployment)
    + [Simple Way](#simple-way)
      - [Instructions](#instructions)
    + [Deploy on VPS](#deploy-on-vps)
      - [Setup `config.env`](#setup-configenv)
        * [Setup rclone](#setup-rclone)
      - [Deploying](#deploying)
    + [The Legacy Way](#the-legacy-way)
  * [Variable Explanations](#variable-explanations)
    + [Mandatory Variables](#mandatory-variables)
    + [Optional Configuration Variables](#optional-configuration-variables)
    + [Available Commands](#available-commands)
  * [How to Use?](#how-to-use)
  * [Credits](#credits-and-thanks-to)

  # Benefits
      ✓ Google Drive link cloning using gclone. (WIP)
      ✓ Telegram File mirrorring to cloud along with its unzipping, unrar and untar
      ✓ Drive/Teamdrive support/All other cloud services rclone.org supports
      ✓ Extract compatible archive
      ✓ Custom file name
      ✓ Custom commands
      ✓ Get total size of your working cloud directory
      ✓ You can also upload files downloaded from /ytdl command to gdrive using `/ytdl gdrive` command.
      ✓ You can also deploy this on your VPS
      ✓ Option to select either video will be uploaded as document or streamable
      ✓ Added /rename command to clear the downloads which are not deleted automatically.
      ✓ Added support for youtube playlist
      ✓ Renaming of Telegram files support added.
      ✓ Changing rclone destination config on fly (By using `/rclone` in private mode)
      
  # To-Do
  -   [ ] Adding mp3 files support while playlist downloading.
  -   [ ] Password support while Unarchiving the files.
  -   [ ] Selection of required files during leeching the big files using aria(/leech command)

  ## Deployment

  ### Simple Way

  #### Instructions 

  **Modified for use on Heroku, please do not heavily abuse!**

  **Join [this](https://t.me/tgleechsupport) Telegram Group if you want support, I will try to help you as much as I can.**

  <p><a href="https://heroku.com/deploy?template=https://github.com/reaitten/tgtlg"> <img src="https://img.shields.io/badge/Deploy%20To%20Heroku-blueviolet?style=for-the-badge&logo=heroku" width="200""/></a></p>

  ## Deploy on VPS

  - Clone this repo:
  ```
  git clone -b main https://github.com/reaitten/tgtlg tgtlg
  cd tgtlg
  ```

  - Install requirements
  For Debian based distros
  ```
  sudo snap install docker
  ```
  Install Docker by following the [official docker docs](https://docs.docker.com/engine/install/debian/)

  ### Setup `config.env`
  ```
  cp sample_config.env config.env
  ```
  After this step you will see a new file named ```config.env``` in root directory.

  Fill those compulsory variables.

  If you need more explanation about any variable then read [app.json](https://github.com/reaitten/tgtlg/blob/deploy-main/app.json)

  ### Setup rclone

  1. Set rclone locally by following the official repo: https://rclone.org/docs/
  2. Get your `rclone.conf` file will look something like this:
  
  ```
  [NAME]
  type = 
  scope =
  token =
  client_id = 
  client_secret = 
  ```
  
  3. Copy `rclone.conf` file in the root directory (Where `Dockerfile` exists).

  4. Your config can contains multiple drive entries. (Default: First one and change using `/rclone` command)

  ### Deploying

  - Start Docker Daemon (skip if already running):
  ```
  sudo dockerd
  ```
  - Build Docker Image:
  ```
  sudo docker build . -t torrentleech-gdrive
  ```
  - Run the image:
  ```
  sudo docker run torrentleech-gdrive
  ```
  Follow this [Video Tutorial](https://youtu.be/J3tMbngA9DE)
  ### The Legacy Way
  Simply clone the repository and run the main file:

  ```
  git clone -b 4forks https://github.com/reaitten/tgtlg
  cd TorrentLeech-Gdrive
  python3 -m venv venv
  . ./venv/bin/activate
  pip install -r requirements.txt
  # Create config.py appropriately
  python3 -m tgtlg
  ```
  ## Variable Explanations

  ### Mandatory Variables

  - `TG_BOT_TOKEN`: Create a bot using [@BotFather](https://telegram.dog/BotFather), and get the Telegram API token.

  - `APP_ID`
  
  - `API_HASH`: Get these two values from [my.telegram.org/apps](https://my.telegram.org/apps).
    * N.B.: if Telegram is blocked by your ISP, try our [Telegram bot](https://telegram.dog/UseTGXBot) to get the IDs.

  - `AUTH_CHANNEL`: Create a Super Group in Telegram, add `@GoogleIMGBot` to the group, and send /id in the chat, to get this value.

  - `OWNER_ID`: ID of the bot owner, He/she can be abled to access bot in bot only mode too(private mode).

  ### Optional Configuration Variables

<details>
      <summary><b>Click Here for more Details</b></summary>


  - `DOWNLOAD_LOCATION`: The location you would like the bot to download to locally.
  - `MAX_FILE_SIZE`:
  - `TG_MAX_FILE_SIZE`:
  - `FREE_USER_MAX_FILE_SIZE`
  - `MAX_TG_SPLIT_FILE_SIZE`:
  - `CHUNK_SIZE`:
  - `MAX_MESSAGE_LENGTH`:
  - `PROCESS_MAX_TIMEOUT`:
  - `ARIA_TWO_STARTED_PORT`:
  - `EDIT_SLEEP_TIME_OUT`:
  - `MAX_TIME_TO_WAIT_FOR_TORRENTS_TO_START`:
  - `FINISHED_PROGRESS_STR`:
  - `UN_FINISHED_PROGRESS_STR`:
  - `TG_OFFENSIVE_API`:
  - `CUSTOM_FILE_NAME`:
  - `LEECH_COMMAND`:
  - `YTDL_COMMAND`:
  - `GYTDL_COMMAND`:
  - `GLEECH_COMMAND`:
  - `TELEGRAM_LEECH_COMMAND`:
  - `TELEGRAM_LEECH_UNZIP_COMMAND`:
  - `PYTDL_COMMAND`:
  - `CLONE_COMMAND_G`:
  - `UPLOAD_COMMAND`:
  - `RENEWME_COMMAND`:
  - `SAVE_THUMBNAIL`:
  - `CLEAR_THUMBNAIL`:
  - `GET_SIZE_G`:

  - `UPLOAD_AS_DOC`: Takes two option True or False. If True file will be uploaded as document. This is for people who wants video files as document instead of streamable.

  - `INDEX_LINK`: (Without `/` at last of the link, otherwise u will get error) During creating index, plz fill `Default Root ID` with the id of your `DESTINATION_FOLDER` after creating. Otherwise index will not work properly.

  - `DESTINATION_FOLDER`: Name of your folder in your respective drive where you want to upload the files using the bot.

</details>

  ### Available Commands

  - `/rclone`: This will change your drive config on fly. (First one will be default)
  - `/gclone`: This command is used to clone gdrive files or folder using gclone.

  - `/help`: To get a list of commands

  - `/leech`: This command should be used as reply to a magnetic link, a torrent link, or a direct link. [this command will SPAM the chat and send the downloads a seperate files if there is more than one file, in the specified torrent]
  - `/archive`: This command should be used as reply to a magnetic link, a torrent link, or a direct link. [This command will create a .tar.gz file of the output directory, and send the files in the chat, splited into PARTS of 1024MiB each, due to Telegram limitations]
  - `/extract`: This will unarchive file and upload to telegram.

  - `/gleech`: This command should be used as reply to a magnetic link, a torrent link, or a direct link. And this will download the files from the given link or torrent and will upload to the cloud using rclone.
  - `/garchive`: This command will compress the folder/file and will upload to your cloud.
  - `/gextract`: This will unarchive file and upload to cloud.
  - `/gclone`: This command is used to clone gdrive files or folder using gclone.

Syntax: `[ID of the file or folder][one space][name of your folder only (If the ID is of file, don't put anything)]` and then reply /gclone to it.

  - `/tleech`: This will mirror the telegram files to your respective cloud.
  - `/textract`: This will unarchive telegram file and upload to cloud.

  - `/ytdl`: This command should be used as reply to a [supported link](https://ytdl-org.github.io/youtube-dl/supportedsites.html)
  - `/pytdl`: This command will download videos from youtube playlist link and will upload to telegram.
  - `/gytdl`: This will download and upload to your cloud.
  - `/gpytdl`: This download youtube playlist and upload to your cloud.
  - `/getsize`: This will give you total size of your destination folder in cloud.
  - `/renewme`: This will clear the remains of downloads which are not getting deleted after upload of the file or after /cancel command.
  - `/rename`: To rename the telegram files.

  - `/rclone`: This will change your drive config on fly. (First one will be default)
  - `/log`: This will send you a txt file of the logs.

Only works with direct link and youtube link for now.
You can add a custom name as it's prefix to the file. Example: if gk.txt uploaded will be what you add in CUSTOM_FILE_NAME + gk.txt

  You can add a custom name as it's prefix of the original file name.
  e.g: if file is `gk.txt` uploaded will be what you added in ``CUSTOM_FILE_NAME`` + ``gk.txt``
  It is like you can add custom name as prefix of the original file name.
  Like if your file name is `gk.txt` uploaded will be what u add in `CUSTOM_FILE_NAME` + `gk.txt`

  ## How to Use?

  * send any one of the available commands, as a reply to a valid link/magnet/torrent.


  ## Credits
  - [GautamKumar](https://github.com/gautamajay52/TorrentLeech-Gdrive)
  - [SpEcHiDe](https://github.com/SpEcHiDe/PublicLeech) for his wonderful code
  - [cihanvol](https://github.com/cihanvol) for [direct_link_generator](https://github.com/reaitten/tgtlg/blob/main/tgtlg/helper_funcs/direct_link_generator.py)
  - [MaxxRider](https://github.com/MaxxRider) for tweaked version of [TorrentLeech-Gdrive](https://github.com/MaxxRider/Leech-Pro)
  - [Rclone Team](https://rclone.org) for theirs awesome tool
  - [Dan Tès](https://telegram.dog/haskell) for his [Pyrogram Library](https://github.com/pyrogram/pyrogram)
  - [Robots](https://telegram.dog/Robots) for their [@UploadBot](https://telegram.dog/UploadBot)
  - [@AjeeshNair](https://telegram.dog/AjeeshNait) for his [torrent.ajee.sh](https://torrent.ajee.sh)
  - [@gotstc](https://telegram.dog/gotstc), @aryanvikash, [@HasibulKabir](https://telegram.dog/HasibulKabir) for their TORRENT groups
