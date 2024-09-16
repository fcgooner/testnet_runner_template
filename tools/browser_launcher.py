import asyncio
import json

from aiohttp import ClientSession, ClientConnectionError, ClientPayloadError, TCPConnector
from asyncio import TimeoutError
from loguru import logger

from classes.ads_profile import Profile
from config import ANTIC_PORT


async def browser_launcher(ads_profile: Profile, start: bool = False) -> str | bool | None:
    profile_id = ads_profile.profile_id
    profile_string = f"PROFILE {ads_profile.profile_number} ({ads_profile.profile_id})"

    if start:
        url = f"http://local.adspower.net:{ANTIC_PORT}/api/v1/browser/start?user_id={profile_id}&open_tabs=1&ip_tab=0"
    else:
        url = f"http://local.adspower.net:{ANTIC_PORT}/api/v1/browser/stop?user_id={profile_id}"

    try:
        for attempt in range(5):
            logger.debug(f"{profile_string} | {attempt + 1} СПРОБА ЗАПУСКУ")

            connector = TCPConnector(limit=200)
            async with ClientSession(connector=connector) as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        try:
                            response_data = await response.json()
                            print(response_data)

                            if start:
                                if response_data.get('code') == 0 and response_data.get('data', {}).get('ws', {}).get('puppeteer'):
                                    connection_url = response_data['data']['ws']['puppeteer']
                                    return connection_url
                            else:
                                if response_data.get('code') == 0:
                                    return True

                        except json.JSONDecodeError as e:
                            logger.error(f"{profile_string} | UNABLE TO DECODE JSON FROM RESPONSE: {e}")
                    else:
                        logger.error(f"{profile_string} | UNABLE TO RETRIEVE DATA. STATUS CODE: {response.status}")

            await asyncio.sleep(3)

    except (ClientConnectionError, ClientPayloadError, TimeoutError) as e:
        logger.error(f"{profile_string} | LAUNCH ERROR: {e}")
    except Exception as e:
        logger.error(f"{profile_string} | UNKNOWN LAUNCH ERROR: {e}")

    return None
