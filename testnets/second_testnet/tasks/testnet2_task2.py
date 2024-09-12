from loguru import logger
from playwright.async_api import Page, TimeoutError

from classes.ads_profile import Profile
from testnets.second_testnet.testnet_data.testnet2_variables import testnet2_task2_url
from tools.tools import check_stuck_wallet_window
from tools.wallet_extension import wallet_operations


async def testnet2_task2(ads_profile: Profile, page: Page) -> bool:
    profile_string = f"ПРОФІЛЬ {ads_profile.profile_number} ({ads_profile.profile_id})"

    # ПЕРЕВІРКА ЧИ НЕ ЗАВИСЛО ВІКНО ГАМАНЦЯ З ПОПЕРЕДНІХ ЗАВДАНЬ. ЯКЩО ЗАВИСЛО - ЗАКРИТИ
    stuck_wallet = await check_stuck_wallet_window(page)
    if stuck_wallet:
        logger.debug(f"{profile_string} | TASK2 | ВІКНО ГАМАНЦЯ ЗАКРИТО АБО ЙОГО НЕ БУЛО")
    else:
        logger.warning(
            f"{profile_string} | TASK2 | НЕ ВДАЛОСЯ ЗАКРИТИ ВІКНО ГАМАНЦЯ. МОЖЛИВІ ПРОБЛЕМИ З ВИКОНАННЯМ ЗАВДАННЯ")

    # ВИКОНАННЯ ЗАВДАННЯ
    url = testnet2_task2_url

    logger.info(f"{profile_string} | TASK2 | ПОЧАТОК ВИКОНАННЯ ЗАВДАННЯ")

    try:
        await page.goto(url)
        logger.success(f"{profile_string} | TASK2 | СТОРІНКА УСПІШНО ЗАВАНТАЖЕНА")
    except TimeoutError as e:
        logger.error(f"{profile_string} | TASK2 | ПОМИЛКА ЗАВАНТАЖЕННЯ СТОРІНКИ: {e}")
        return False

    # ПРИКЛАД ПІД'ЄДАННЯ ГАМАНЦЯ ДО САЙТУ
    connect_successful = await wallet_operations(page=page, operation='connect')
    if not connect_successful:
        logger.error(f"{profile_string} | TASK2 | НЕ ВДАЛОСЯ ПІД'ЄДНАТИ ГАМАНЕЦЬ")
        return False

    # ПРИКЛАД ПІДПИСАННЯ ТРАНЗАКЦІЇ
    sign_successful = await wallet_operations(page=page, operation='sign')
    if not sign_successful:
        logger.error(f"{profile_string} | TASK2 | НЕ ВДАЛОСЯ ПІДПИСАТИ ТРАНЗАКЦІЮ")
        return False

    return True
