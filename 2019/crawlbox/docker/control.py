import asyncio
import argparse
import requests
from pyppeteer import connect
from pyppeteer.browser import Browser
from pyppeteer.page import Page

loop = asyncio.get_event_loop()
base = 'http://127.0.0.1:21218'
data = requests.get(f'{base}/json/version').json()

browser: Browser = loop.run_until_complete(connect(browserWSEndpoint=data['webSocketDebuggerUrl'], logLevel='WARNING'))


async def show_tabs_command():
    for tab in await browser.pages():
        print('%r, %r' % (tab.url, await tab.title()))


async def page_source_command():
    for tab in await browser.pages():
        print('%r' % tab.url)
        print('%r' % await tab.content())
        print('\n==============================\n')


async def main():
    parser = argparse.ArgumentParser(description='Control RWCTF Crawlbox Game.')
    subcommands = parser.add_subparsers(dest='command_name')
    subcommands.add_parser('show_tabs')
    subcommands.add_parser('page_source')
    kwargs = parser.parse_args()

    if getattr(kwargs, 'command_name', ''):
        func = getattr(kwargs, 'command_name') + '_command'
        await globals()[func]()

    await browser.disconnect()


if __name__ == '__main__':
    loop.run_until_complete(main())
