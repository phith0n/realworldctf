FROM python:3.7-alpine

LABEL maintainer="phith0n <root@leavesongs.com>"

ADD requirements.txt /tmp/requirements.txt
ADD flag/readflag.c /tmp/readflag.c
ENV PYCURL_SSL_LIBRARY=openssl

RUN set -ex \
    # && sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories \
    && apk add --no-cache libcurl postgresql-dev

RUN set -ex \
    && apk add --no-cache --virtual .build-deps build-base curl-dev linux-headers \
    # && pip install -i https://mirrors.aliyun.com/pypi/simple -r /tmp/requirements.txt \
    && pip install -r /tmp/requirements.txt \
    && gcc /tmp/readflag.c -o /readflag \
    && apk del --no-cache --purge .build-deps \
    && rm -rf /var/cache/apk/* /tmp/*

COPY ./code/ /usr/src/
WORKDIR /usr/src/rwctf

COPY flag/flag /flag
RUN set -ex \
    && chown root:root -R . \
    && chown root:root /flag \
    && chmod 0600 /flag \
    && chmod u+s /readflag

CMD ["sh", "server.sh"]
