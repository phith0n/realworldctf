#!/usr/bin/env bash

setuser chrome google-chrome --remote-debugging-port=21218 \
    --disable-background-networking --disable-background-timer-throttling --disable-breakpad \
    --disable-browser-side-navigation --disable-client-side-phishing-detection --disable-default-apps \
    --disable-dev-shm-usage --disable-extensions --disable-features=site-per-process --disable-hang-monitor \
    --disable-popup-blocking --disable-prompt-on-repost --disable-sync --disable-translate --metrics-recording-only \
    --no-first-run --safebrowsing-disable-auto-update --enable-automation --password-store=basic \
    --use-mock-keychain --headless --hide-scrollbars --mute-audio --disable-gpu \
    --user-agent="Scrapy/ChromeHeadless (+https://scrapy.org)"
