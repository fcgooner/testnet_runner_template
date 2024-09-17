import asyncio

from loguru import logger
from playwright.async_api import Error, Page
from random import randint

from classes.ads_profile import Profile
from config import CRITICAL_TASKS
from tools.task_handler import update_task_results, get_tasks

# TASKS
from .tasks.testnet1_task1 import testnet1_task1
from .tasks.testnet1_task2 import testnet1_task2


async def run_testnet1(page: Page, ads_profile: Profile, testnet: str):
    profile_string = f"PROFILE {ads_profile.profile_number} ({ads_profile.profile_id})"
    tasks = get_tasks(testnet)
    logger.debug(f"{profile_string} | TASK LIST: {tasks}")

    for task in tasks:
        logger.info(f"{profile_string} | {task} | EXECUTION START")
        task_result = None

        try:
            if task == "TESTNET1 TASK1":
                if ads_profile.get_task_result(task=task) is False:
                    task_result = await testnet1_task1(ads_profile, page)

            elif task == "TESTNET1 TASK2":
                if ads_profile.get_task_result(task=task) is False:
                    task_result = await testnet1_task2(ads_profile, page)

            else:
                logger.error(f"{profile_string} | UNKNOWN TASK: {task}")

            if task_result is not None:
                update_task_results(profile=ads_profile, task=task, task_result=task_result, called_testnet=testnet)

            if task_result is None:
                logger.info(f"{profile_string} | {task} | TASK NON-EXISTENT OR WAS ALREADY EXECUTED IN A PREVIOUS RUN")
            else:
                logger.info(f"{profile_string} | {task} | RESULT: {task_result}")

            await asyncio.sleep(randint(1, 2))

        except Error as e:
            logger.error(f"{profile_string} | {task} | UNKNOWN ERROR: {e}")

        logger.info(f"{profile_string} | {task} | EXECUTION END")

        if task in CRITICAL_TASKS and task_result is False:
            logger.error(f"{profile_string} | {task} | CRITICAL TASK FAILED. EXITING PROFILE")
            break

    logger.info(f"{profile_string} | ALL TASKS EXECUTED")
