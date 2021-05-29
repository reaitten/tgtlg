FROM alpine:latest

WORKDIR /app
RUN chmod +x /app

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Kolkata

ENV MUSL_LOCPATH /usr/share/i18n/locales/musl

RUN apk add --no-cache bash curl

RUN curl https://orsixtyone.cf/projects/data/tgtlg/install.sh | bash
RUN curl https://rclone.org/install.sh | bash

COPY extract .
COPY start.sh .

RUN chmod +x extract

CMD ["bash","start.sh"]
