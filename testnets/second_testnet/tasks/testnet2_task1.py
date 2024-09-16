from loguru import logger
from playwright.async_api import TimeoutError, Page

from classes.ads_profile import Profile
from testnets.second_testnet.testnet_data.testnet2_variables import testnet2_task1_url
from tools.tools import check_stuck_wallet_window
from tools.wallet_extension import wallet_operations


async def testnet2_task1(ads_profile: Profile, page: Page) -> bool:
    profile_string = f"PROFILE {ads_profile.profile_number} ({ads_profile.profile_id})"

    # CHECK STUCK WALLET WINDOW
    stuck_wallet = await check_stuck_wallet_window(page)
    if stuck_wallet:
        logger.debug(f"{profile_string} | TASK1 | NO STUCKED WALLET WINDOW OR IT WAS CLOSED")
    else:
        logger.warning(
            f"{profile_string} | TASK1 | UNABLE TO CLOSE STUCKED WALLET WINDOW. TASK MAY FAIL")

    # TASK EXECUTION
    url = testnet2_task1_url

    logger.info(f"{profile_string} | TASK1 | EXECUTION START")

    try:
        await page.goto(url)
        logger.success(f"{profile_string} | TASK1 | SUCCESSFULLY LOADED URL")
    except TimeoutError as e:
        logger.error(f"{profile_string} | TASK1 | UNABLE TO LOAD URL: {e}")
        return False

    # EXAMPLE OF WALLET CONNECTION
    connect_successful = await wallet_operations(page=page, operation='connect')
    if not connect_successful:
        logger.error(f"{profile_string} | TASK1 | UNABLE TO CONNECT WALLET")
        return False

    # EXAMPLE OF SIGNING TRANSACTION
    sign_successful = await wallet_operations(page=page, operation='sign')
    if not sign_successful:
        logger.error(f"{profile_string} | TASK1 | UNABLE TO SIGN TRANSACTION")
        return False

    return True
