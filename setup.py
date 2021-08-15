import setuptools

setuptools.setup(
    name="tgtlg",
    version="1.3.4",
    author="reaitten",
    author_email="wsy0xf2u8@relay.firefox.com",
    description="A Telegram Torrent (and youtube-dl) Leecher based on Pyrogram.",
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    include_package_data=True,
    python_requires=">=3.8.2",
    url="https://github.com/reaitten/tgtlg",
    project_urls={
        "Bug Tracker": "https://github.com/reaitten/tgtlg/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Operating System :: POSIX :: Linux",
        "Development Status :: 5 - Production/Stable"
    ],
    packages=setuptools.find_packages(),
    install_requires=[
        'wheel', 
        'rust', 
        'aiohttp', 
        'aria2p==0.9.1', 
        'hachoir', 
        'Pillow', 
        'Pyrogram', 
        'tgcrypto', 
        'youtube_dl', 
        'hurry.filesize', 
        'python-telegram-bot', 
        'python-dotenv', 
        'beautifulsoup4>=4.8.2,<4.8.10', 
        'requests', 
        'messages', 
        'js2py'],
    scripts=['extract'],
    entry_points={
        "console_scripts":[
            "tgtlg = tgtlg.__main__:main"
                ],
    },
)
