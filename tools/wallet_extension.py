import asyncio

from loguru import logger
from playwright.async_api import Page, TimeoutError

from config import MAX_WALLET_RETRIES


async def wallet_operations(page: Page, operation: str, password: str = "") -> bool:
    rabby_wallet = "notification.html"

    for attempt in range(MAX_WALLET_RETRIES):
        await page.wait_for_timeout(timeout=2000)

        all_pages = page.context.pages
        for tab in all_pages:
            if rabby_wallet in tab.url:
                if operation == "unlock":
                    try:
                        await tab.locator("[type=password]").fill(password)
                        await tab.locator("[type=submit]").click()
                        return True
                    except TimeoutError as e:
                        logger.error(f"ERROR DURING WALLET UNLOCK: {e}")
                        return False

                elif operation == "sign":
                    try:
                        await tab.get_by_text(text="Sign", exact=True).click()
                        await tab.locator("text=Confirm").click()
                        return True
                    except TimeoutError as e:
                        print(f"ERROR DURING TRANSACTION SIGN: {e}")
                        return False

                elif operation == "connect":
                    try:
                        connect_locator = tab.get_by_text("Ignore all")
                        if await connect_locator.count() == 1:
                            await connect_locator.click()
                        await asyncio.sleep(3)
                        await tab.get_by_role(role="button", name="Connect").click()
                        return True
                    except TimeoutError as e:
                        print(f"ERROR DURING WALLET CONNECTION: {e}")
                        return False

    return False
