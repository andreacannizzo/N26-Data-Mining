import asyncio
from time import sleep

from pyppeteer import launch


async def main():
    browser = await launch(
        headless=False,
        handleSIGINT=False,
        handleSIGTERM=False,
        handleSIGHUP=False,
    )
    sleep(3)
    page = await browser.newPage()
    sleep(3)
    await page.goto('https://app.n26.com/login')
    sleep(3)
    
    sleep(600)
    # await browser.close()

asyncio.get_event_loop().run_until_complete(main())