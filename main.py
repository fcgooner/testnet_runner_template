import asyncio
import sys

from datetime import datetime
from loguru import logger
from random import randint
from time import sleep

from config import CONTINUE_RUN, LOG_LEVEL, MAX_TASK_ATTEMPTS, TESTNET_TASKS_DATAFILES
from data.variables import ALL_TASKS, DARK_GRAY
from run_testnets import run_testnets
from tools.profiles_handler import get_profiles_to_run, initialize_profiles
from tools.task_handler import update_task_csv


async def main():

    if CONTINUE_RUN:
        logger.critical(f"ЦЕ НЕ НУЛЬОВИЙ ЗАПУСК: CONTINUE_RUN is {CONTINUE_RUN}")

    # ОБНУЛЯЄМО РЕЗУЛЬТАТИ ЗАВДАНЬ ПЕРЕД ЗАПУСКОМ ПРОФІЛІВ
    else:
        for testnet in TESTNET_TASKS_DATAFILES:
            filepath = TESTNET_TASKS_DATAFILES[testnet]
            update_task_csv(csv_file_path=filepath)
        logger.info("CSV-таблиці завдань скинуто")

    # ОТРИМУЄМО СПИСОК ПРОФІЛІВ
    original_profile_list, shuffled_profile_list = initialize_profiles()

    for cycle in range(1, MAX_TASK_ATTEMPTS + 1):
        if cycle > 1:
            logger.info("Спимо між прогоном нової пачки профілів")
            await asyncio.sleep(randint(30, 60))

        all_profiles = shuffled_profile_list.copy()
        logger.debug(f"ЦИКЛ {cycle}/{MAX_TASK_ATTEMPTS}")

        while True:
            try:
                profiles_to_run = get_profiles_to_run(cycle, all_profiles)
                async_tasks = [asyncio.create_task(run_testnets(ads_profile)) for ads_profile in profiles_to_run]

                if not async_tasks:
                    logger.debug(f"УСІ ПРОФІЛІ ВІДПРАЦЬОВАНО")
                    break

                # ЗАПУСК ВИБРАНИХ ПРОФІЛІВ
                logger.debug("ЗАПУСК ПАЧКИ ПРОФІЛІВ")
                await asyncio.wait(async_tasks)

                # ОНОВЛЮЄМО СПИСОК НЕВІДПРАЦЬОВАНИХ ПРОФІЛІВ
                all_profiles = [item for item in all_profiles if item not in profiles_to_run]
                if not all_profiles:
                    break

                sleep(randint(30, 60))
            except Exception as e:
                logger.critical(f"НЕВІДОМА ПОМИЛКА: {e}")

    # ВИВЕСТИ РЕЗУЛЬТАТИ ЗАВДАНЬ ДЛЯ КОЖНОГО ПРОФІЛЯ В КОНСОЛЬ
    task_summary = {}
    for profile in original_profile_list:
        profile.print_task_results()

        for task, result in profile.task_results.items():
            if task in ALL_TASKS:
                task_summary[task] = task_summary.get(task, 0) + (1 if result is True else 0)

    # ВИВЕДЕННЯ ЗВЕДЕНИХ РЕЗУЛЬТАТІВ ЗАВДАНЬ ПО ВСІХ ПРОФІЛЯХ В КОНСОЛЬ
    max_task_name_length = max(len(task) for task in task_summary)

    logger.log("PRINTOUT_BLUE", f'\nЗВЕДЕНІ РЕЗУЛЬТАТИ:')
    for task in task_summary:
        logger.log("PRINTOUT_YELLOW", f"  {task.ljust(max_task_name_length)}: {task_summary[task]}/{len(original_profile_list)}")

    if CONTINUE_RUN:
        logger.critical(f"ЦЕ НЕ НУЛЬОВИЙ ЗАПУСК: CONTINUE_RUN is {CONTINUE_RUN}")


def logger_format(record):
    base_format = "{time:DD-MM-YYYY | HH:mm:ss} | {level}"
    message = "{message}"
    error_function = ""

    if record["level"].name == "ERROR":
        error_function = f" | {record['function']}()"

    if record["level"].name in ['PRINTOUT_BLUE', 'PRINTOUT_GREEN', 'PRINTOUT_RED', 'PRINTOUT_YELLOW']:
        return f"{message}\n"

    return f"{base_format}{error_function} | {message}\n"


if __name__ == "__main__":
    # ІНІЦІАЛІЗАЦІЯ ЛОҐҐЕРА
    logger.remove()
    logger.level("DEBUG", color=DARK_GRAY)
    logger.level("PRINTOUT_BLUE", no=25, color="<blue>")
    logger.level("PRINTOUT_GREEN", no=25, color="<green>")
    logger.level("PRINTOUT_RED", no=25, color="<red>")
    logger.level("PRINTOUT_YELLOW", no=25, color="<yellow>")

    # ЛОҐҐЕР ДЛЯ КОНСОЛІ
    logger.add(
        sink=sys.stdout,
        format="<level>{message}</level>",
        level=LOG_LEVEL,
        colorize=True
    )

    # ЛОҐҐЕР ДЛЯ ФАЙЛА
    current_time = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    logger.add(
        sink=f'logs/{current_time}.log',
        format=logger_format,
        level=LOG_LEVEL
    )

    asyncio.run(main())
