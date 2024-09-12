from loguru import logger
from playwright.async_api import async_playwright
from random import shuffle

from classes.ads_profile import Profile
from config import TESTNET_TASKS_DATAFILES, WALLET_NAMES
from tools.tools import wallet_unlock
from tools.browser_launcher import browser_launcher

# ТЕСТНЕТИ
from testnets.first_testnet.first_testnet import run_testnet1
from testnets.second_testnet.second_testnet import run_testnet2


async def run_testnets(ads_profile: Profile):
    profile_str = f"ПРОФІЛЬ {ads_profile.profile_number} ({ads_profile.profile_id})"

    # ПЕРЕМІШУВАННЯ СПИСКУ ТЕСТНЕТІВ
    testnets_list = []
    for testnet in TESTNET_TASKS_DATAFILES:
        testnets_list.append(testnet)

    shuffle(testnets_list)
    logger.debug("ТЕСТНЕТИ ПЕРЕМІШАНО")

    # РОБОТА З ПРОФІЛЕМ
    logger.info(f"{profile_str} | ПОЧАТОК РОБОТИ")

    connect_url = await browser_launcher(ads_profile, start=True)

    if isinstance(connect_url, str):
        # ЛІНК ДЛЯ ПІД'ЄДНАННЯ ОТРИМАНО
        async with async_playwright() as p:
            browser = await p.chromium.connect_over_cdp(connect_url)
            context = browser.contexts[0]
            page = await context.new_page()

            # РОЗБЛОКУВАННЯ ГАМАНЦІВ ПЕРЕД ПОЧАТКОМ ВИКОНАННЯ ЗАВДАНЬ
            wallet_unlocked = await wallet_unlock(page=page,
                                                  wallet_names=WALLET_NAMES,
                                                  wallet_pass=ads_profile.wallet_pass)

            if not isinstance(wallet_unlocked, bool):
                logger.error(f"{profile_str} | НЕ ВДАЛОСЯ РОЗБЛОКУВАТИ ГАМАНЕЦЬ: {wallet_unlocked}")
                return

            logger.debug(f"{profile_str} | ГАМАНЕЦЬ РОЗБЛОКОВАНО")

            for testnet in testnets_list:
                try:
                    if testnet == 'TESTNET 1':
                        await run_testnet1(page=page, ads_profile=ads_profile, testnet=testnet)

                    elif testnet == 'TESTNET 2':
                        await run_testnet2(page=page, ads_profile=ads_profile, testnet=testnet)

                except Exception as e:
                    logger.error(f"{profile_str} | ПОМИЛКА ПІД ЧАС ВИКОНАННЯ {testnet}: {e}")

            # sleep(100000)

            browser_closed = await browser_launcher(ads_profile)
            if isinstance(browser_closed, bool) and browser_closed:
                logger.debug(f"{profile_str} | БРАУЗЕР ЗАКРИТО")
            else:
                logger.error(f"{profile_str} | НЕ ВДАЛОСЯ ЗАКРИТИ БРАУЗЕР")

    else:
        logger.error(f"{profile_str} | НЕ ВДАЛОСЯ ЗАПУСТИТИ БРАУЗЕР")

    logger.info(f"{profile_str} | КІНЕЦЬ РОБОТИ")
