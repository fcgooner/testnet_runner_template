import asyncio

from loguru import logger
from playwright.async_api import Error, Page
from random import randint

from classes.ads_profile import Profile
from config import CRITICAL_TASKS
from tools.task_handler import update_task_results, get_tasks

# TASKS
from .tasks.testnet2_task1 import testnet2_task1
from .tasks.testnet2_task2 import testnet2_task2


async def run_testnet2(page: Page, ads_profile: Profile, testnet: str):
    profile_string = f"ПРОФІЛЬ {ads_profile.profile_number} ({ads_profile.profile_id})"
    tasks = get_tasks(testnet)
    logger.debug(f"{profile_string} | СПИСОК ЗАВДАНЬ: {tasks}")

    for task in tasks:
        logger.info(f"{profile_string} | {task} | ПОЧАТОК ВИКОНАННЯ")
        task_result = None

        try:
            if task == "TESTNET2 TASK1":
                if ads_profile.get_task_result(task=task) is False:
                    task_result = await testnet2_task1(ads_profile, page)

            elif task == "TESTNET2 TASK2":
                if ads_profile.get_task_result(task=task) is False:
                    task_result = await testnet2_task2(ads_profile, page)

            else:
                logger.error(f"{profile_string} | НЕВІДОМЕ ЗАВДАННЯ: {task}")

            if task_result is not None:
                update_task_results(profile=ads_profile, task=task, task_result=task_result, called_testnet=testnet)

            await asyncio.sleep(randint(1, 2))

        except Error as e:
            logger.error(f"{profile_string} | {task} | НЕВІДОМА ПОМИЛКА: {e}")

        logger.info(f"{profile_string} | {task} | РЕЗУЛЬТАТ: {task_result}")
        logger.info(f"{profile_string} | {task} | КІНЕЦЬ ВИКОНАННЯ")

        if task in CRITICAL_TASKS and task_result is False:
            logger.error(f"{profile_string} | {task}={task_result} | CRITICAL_TASKS={CRITICAL_TASKS}")
            break

    logger.info(f"{profile_string} | КІНЕЦЬ ВИКОНАННЯ УСІХ ЗАВДАНЬ")
