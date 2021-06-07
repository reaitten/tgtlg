import setuptools

setuptools.setup(
    name="tgtlg",
    version="1.2.6",
    author="reaitten",
    author_email="riojosepha@gmail.com",
    description="A Telegram Bot written in Python language to mirror files on the internet to a Cloud Provider using rclone.",
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/reaitten/tgchizu",
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
