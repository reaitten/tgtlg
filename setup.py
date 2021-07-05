import setuptools

setuptools.setup(
    name="tgtlg",
    version="1.2.9",
    author="reaitten",
    author_email="wsy0xf2u8@relay.firefox.com",
    description="A Telegram Torrent (and youtube-dl) Leecher based on Pyrogram.",
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/reaitten/tgtlg",
    project_urls={
        "Bug Tracker": "https://github.com/reaitten/tgtlg/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
        "Development Status :: 5 - Production/Stable"
    ],
    packages=setuptools.find_packages(),
    install_requires=open('requirements.txt', 'r', encoding='utf-8').read().split('\n'),
    scripts=['extract'],
    python_requires=">=3.8.2",
)
