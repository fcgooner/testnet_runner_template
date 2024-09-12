import csv

from loguru import logger
from random import shuffle, randint

from classes.ads_profile import Profile
from config import TESTNET_TASKS_DATAFILES, TESTNET_TASKS


def update_task_results(profile: Profile, task: str, task_result: bool, called_testnet: str) -> None:
    # ОНОВЛЕННЯ РЕЗУЛЬТАТІВ ЗАВДАННЯ
    profile.set_task_result(task.upper(), task_result)

    for testnet in TESTNET_TASKS_DATAFILES:
        filepath = TESTNET_TASKS_DATAFILES[testnet]

        if called_testnet.lower() in filepath:
            task_name = task.split()[-1]
            update_task_csv(
                csv_file_path=filepath,
                profile_id=profile.profile_id,
                column_name=task_name.upper(),
                new_value=str(task_result)
            )
            logger.debug(
                f"ПРОФІЛЬ {profile.profile_number} ({profile.profile_id}) | {task} | РЕЗУЛЬТАТ ({task_result}) ЗАПИСАНО В ТАБЛИЦЮ")
            return


def update_task_csv(csv_file_path, profile_id=None, column_name=None, new_value=None):
    updated_rows = []

    with open(csv_file_path, mode='r', newline='') as csvfile:
        csvreader = csv.DictReader(csvfile)

        for row in csvreader:
            updated_row = {'PROFILE_ID': row['PROFILE_ID']}  # PROFILE_ID ЗАЛИШАЄМО НЕЗМІННИМ
            for key in row.keys():
                if key == 'PROFILE_ID':
                    continue
                # ОНОВЛЮЄМО ЛИШЕ КОНКРЕТНЕ ЗАВДАННЯ
                if profile_id and column_name and new_value is not None:
                    if row['PROFILE_ID'] == profile_id and key == column_name:
                        updated_row[key] = new_value # ЗАПИСУЄМО НОВЕ ЗНАЧЕННЯ
                    else:
                        updated_row[key] = row[key]  # ЗАЛИШАЄМО СТАРЕ ЗНАЧЕННЯ
                # ОЧИЩЕННЯ ВСІЄЇ ТАБЛИЦІ
                else:
                    updated_row[key] = 'False'

            updated_rows.append(updated_row)

    # ЗАПИСУЄМО ОНОВЛЕНІ РЯДКИ
    with open(csv_file_path, mode='w', newline='') as csvfile:
        fieldnames = updated_rows[0].keys()
        csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)

        csvwriter.writeheader()
        csvwriter.writerows(updated_rows)


def get_tasks(testnet: str) -> list[str]:
    testnet_core_tasks = []
    testnet_optional_tasks = []
    testnet_group_tasks = []

    # ОТРИМУЄМО СПИСОК CORE ЗАВДАНЬ
    for task in TESTNET_TASKS[testnet.upper()]['CORE']:
        testnet_core_tasks.append(task)

    # ОТРИМУЄМО СПИСОК OPTIONAL ЗАВДАНЬ
    for task in TESTNET_TASKS[testnet.upper()]['OPTIONAL']:
        testnet_optional_tasks.append(task)

    # ОТРИМУЄМО СПИСОК GROUP ЗАВДАНЬ
    for task in TESTNET_TASKS[testnet.upper()]['GROUP']:
        testnet_group_tasks.append(task)

    # ПЕРЕМІШУЄМО OPTIONAL ЗАВДАННЯ
    shuffle(testnet_optional_tasks)

    # ВСТАВЛЯЄМО GROUP ЗАВДАННЯ В РАНДОМНЕ МІСЦЕ СЕРЕД OPTIONAL ЗАВДАНЬ
    random_index = randint(0, len(testnet_optional_tasks))

    testnet_optional_tasks = (
            testnet_optional_tasks[:random_index] +
            testnet_group_tasks +
            testnet_optional_tasks[random_index:]
    )

    # ФОРМУЄМО ФІНАЛЬНИЙ СПИСОК ЗАВДАНЬ
    tasks = testnet_core_tasks + testnet_optional_tasks

    return tasks