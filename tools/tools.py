import asyncio

from playwright.async_api import Page, TimeoutError

from data.variables import rabby_extension_url


# Перевірка чи не застрягло вікно гаманця
async def check_stuck_wallet_window(page: Page):
    await asyncio.sleep(2)
    all_pages = page.context.pages
    for tab in all_pages:
        if "notification.html" in tab.url:
            try:
                await tab.close()
                return True
            except TimeoutError:
                return False

    return True


async def wallet_unlock(page: Page, wallet_names: list[str], wallet_pass: str) -> bool:
    rabby_unlocked = None
    # okx_unlocked = None
    # phantom_unlocked = None

    for wallet_name in wallet_names:
        # RABBY WALLET
        if wallet_name == "RABBY":
            try:
                await page.goto(rabby_extension_url)
                await page.locator("[type=password]").fill(wallet_pass)
                await page.locator("[type=submit]").click()

                rabby_unlocked = True
            except TimeoutError as e:
                rabby_unlocked = e

        # OKX WALLET UNLOCK
        elif wallet_name == "OKX":
            pass

        # PHANTOM WALLET
        elif wallet_name == "PHANTOM":
            pass

    return rabby_unlocked  # okx_unlocked, phantom_unlocked
