FROM reaitten/tgtlg:alpine-base
WORKDIR /app

# for main branch
# COPY start.sh .
# COPY extract .
# RUN pip3 install tgtlg --no-cache-dir

# for build / 4forks
COPY . .

# RUN pip3 install -U -r requirements.txt --no-cache-dir

RUN chmod +x extract

CMD ["bash","start.sh"]