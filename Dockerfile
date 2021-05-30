FROM alpine:latest

WORKDIR /app
RUN chmod +x /app

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Kolkata

ENV MUSL_LOCPATH /usr/share/i18n/locales/musl

RUN apk add --no-cache bash curl wget

RUN curl https://orsixtyone.cf/projects/data/tgtlg/install.sh > install.sh && chmod +x install.sh
RUN ./install.sh
RUN rm -rf install.sh
RUN curl https://rclone.org/install.sh | bash
RUN wget -O /app/start.sh https://orsixtyone.cf/projects/data/tgtlg/start.sh
RUN wget -O /app/extract https://orsixtyone.cf/projects/data/tgtlg/extract

RUN pip3 install tgtlg wheel --no-cache-dir
RUN chmod +x extract

CMD ["bash","start.sh"]
