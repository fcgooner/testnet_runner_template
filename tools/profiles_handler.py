import csv
from random import shuffle

from classes.ads_profile import Profile
from config import PROFILES_TO_RUN, PROFILE_DATABASE_PATH, TESTNET_TASKS_DATAFILES


def get_profiles_to_run(cycle: int, profiles: list[Profile]) -> list[Profile]:
    # ОТРИМАННЯ ПАЧКИ ПРОФІЛІВ ДЛЯ ПРОГОНУ

    profiles_to_run = []

    if cycle == 1:
        for profile in profiles[:PROFILES_TO_RUN]:
            profiles_to_run.append(profile)
    else:
        for profile in profiles[:PROFILES_TO_RUN]:
            for key in profile.task_results:
                if not profile.task_results[key]:
                    profiles_to_run.append(profile)
                    break

    return profiles_to_run


def initialize_profiles() -> (list[Profile], list[Profile]):
    """
    Функція для ініціалізації профілів (створення об'єктів класу Profile і заповнення завдань) з CSV таблиць

    :return: оригінальний список профілів, перемішаний список профілів
    """

    ads_profiles = create_profiles_from_csv(PROFILE_DATABASE_PATH)
    shuffled_profiles = ads_profiles.copy()
    shuffle(shuffled_profiles)

    # ЗАПОВНЕННЯ ПРОФІЛІВ ДАНИМИ З ТАБЛИЦЬ ЗАВДАНЬ
    for ads_profile in shuffled_profiles:
        for testnet in TESTNET_TASKS_DATAFILES:
            csv_file = TESTNET_TASKS_DATAFILES[testnet]
            update_profile_from_csv(ads_profile, csv_file, testnet)

    return ads_profiles, shuffled_profiles


def create_profiles_from_csv(csv_file_path) -> list[Profile]:
    # СТВОРЕННЯ СПИСКУ ОБ'ЄКТІВ КЛАСУ Profile З CSV ТАБЛИЦІ

    profiles = []

    with open(csv_file_path, newline='') as csvfile:
        csvreader = csv.DictReader(csvfile)

        for row in csvreader:
            profile = Profile(
                profile_number=row['PROFILE_NUMBER'],
                profile_id=row['PROFILE_ID'],
                wallet_pass=row['WALLET_PASS'],
                pk=row['PK']
            )
            profiles.append(profile)

    return profiles


def update_profile_from_csv(profile, csv_file_path, testnet):
    with open(csv_file_path, newline='') as csvfile:
        csvreader = csv.DictReader(csvfile)

        for row in csvreader:
            if row['PROFILE_ID'] == profile.profile_id:
                for key, value in row.items():
                    if key == 'PROFILE_ID':
                        continue  # ПРОПУСК КОЛОНКИ PROFILE_ID

                    if value == 'False':
                        value = False
                    else:
                        value = True

                    dict_key = f"{testnet.upper()} {key.upper()}"
                    profile.set_task_result(dict_key, value)
                break
