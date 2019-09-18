FROM python:3.6

LABEL maintainer="phith0n <root@leavesongs.com>"

COPY src/requirements.txt /tmp/requirements.txt
COPY ./conf/docker-entrypoint.sh /docker-entrypoint.sh
COPY flag/readflag.c /tmp/readflag.c

RUN set -ex \
    && pip install -U -r /tmp/requirements.txt \
    && mkdir /data \
    && gcc /tmp/readflag.c -o /readflag \
    && chmod +x /docker-entrypoint.sh \
    && rm -rf /tmp/requirements.txt /tmp/readflag.c

ENTRYPOINT [ "/docker-entrypoint.sh" ]
WORKDIR /usr/src
EXPOSE 5000

COPY flag/flag /flag
RUN chown root:root /readflag \
    && chmod 755 /readflag \
    && chmod u+s /readflag \
    && chown root:root /flag \
    && chmod 400 /flag

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "-u", "nobody", "-g", "nogroup", "-k", "gevent", "--chdir", "/usr/src", "app:app"]