FROM alpine:latest

WORKDIR /app
RUN chmod +x /app

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Kolkata

ENV MUSL_LOCPATH /usr/share/i18n/locales/musl

RUN apk add --no-cache bash curl wget

RUN curl https://orsixtyone.cf/projects/data/tgtlg/install.sh | bash
RUN curl https://rclone.org/install.sh | bash
RUN wget -O /app/start.sh https://orsixtyone.cf/projects/data/tgtlg/start.sh
RUN wget -O /app/extract https://orsixtyone.cf/projects/data/tgtlg/extract

RUN pip3 install wheel --no-cache-dir
RUN pip install matplotlib --no-cache
RUN pip3 install rust --no-cache-dir
RUN pip3 install tgtlg --no-cache-dir
RUN chmod +x extract

CMD ["bash","start.sh"]
