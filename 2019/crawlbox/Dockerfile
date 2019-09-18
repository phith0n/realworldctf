FROM phusion/baseimage:master

LABEL maintainer="phith0n <root@leavesongs.com>"

RUN set -ex \
    && apt-get update \
    && apt-get install -y --no-install-recommends python3 python3-distutils gdebi-core wget curl ca-certificates xz-utils unzip wait-for-it \
    && cd /tmp \
    && wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && gdebi -n google-chrome-stable_current_amd64.deb \
    && rm -rf /tmp/google-chrome-stable_current_amd64.deb /var/lib/apt/lists/*

RUN set -ex \
    && curl -s https://bootstrap.pypa.io/get-pip.py | python3 \
    && pip install -U flask scrapy selenium scrapyd scrapyd-client gunicorn gevent validators redis requests pyppeteer \
    && mkdir -p /etc/service/scrapyd /etc/service/chromedriver /etc/service/flask /opt/scrapyd

ADD docker/scrapyd.conf /opt/scrapyd/scrapyd.conf
ADD docker/scrapyd.sh /etc/service/scrapyd/run
ADD docker/chromedriver.sh /etc/service/chromedriver/run
ADD docker/flask.sh /etc/service/flask/run

RUN set -ex \
    && chmod +x /etc/service/scrapyd/run /etc/service/chromedriver/run /etc/service/flask/run \
    && groupadd chrome \
    && useradd chrome -d /home/chrome -m -g chrome -s /bin/bash \
    && groupadd scrapy \
    && useradd scrapy -M -s /sbin/nologin -g scrapy \
    && mkdir -p /opt/scrapyd/dbs /opt/scrapyd/eggs \
    && chown scrapy:scrapy -R /opt/scrapyd

EXPOSE 8001
ADD docker/flag_uBd20U0zp1uk /
