FROM alpine:latest

WORKDIR /app
RUN chmod +x /app

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Kolkata

ENV MUSL_LOCALE_DEPS cmake make musl-dev gcc gettext-dev libintl 
ENV MUSL_LOCPATH /usr/share/i18n/locales/musl

RUN apk update&& \
	apk add --no-cache \
    $MUSL_LOCALE_DEPS \
    && wget https://gitlab.com/rilian-la-te/musl-locales/-/archive/master/musl-locales-master.zip \
    && unzip musl-locales-master.zip \
      && cd musl-locales-master \
      && cmake -DLOCALE_PROFILE=OFF -D CMAKE_INSTALL_PREFIX:PATH=/usr . && make && make install \
      && cd .. && rm -r musl-locales-master

RUN apk add --no-cache git aria2 wget curl busybox unzip unrar tar python3 python3-dev py-pip py3-pip py3-yarl ffmpeg bash alpine-sdk build-base jpeg-dev zlib-dev

RUN curl https://rclone.org/install.sh | bash

RUN mkdir -p /tmp/ && \
    cd /tmp/ && \
    wget -O /tmp/rarlinux.tar.gz http://www.rarlab.com/rar/rarlinux-x64-6.0.0.tar.gz && \
    tar -xzvf rarlinux.tar.gz && \
    cd rar && \
    cp -v rar unrar /usr/bin/ && \
    rm -rf /tmp/rar*

RUN mkdir /app/gautam
RUN wget -O /app/gautam/gclone.gz https://git.io/JJMSG && gzip -d /app/gautam/gclone.gz
RUN chmod 0775 /app/gautam/gclone

RUN pip3 install -U tgtlg wheel --no-cache-dir

COPY extract .
COPY start.sh .

RUN chmod +x extract

CMD ["bash","start.sh"]
