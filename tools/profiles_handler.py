import csv
from random import shuffle

from classes.ads_profile import Profile
from config import PROFILES_TO_RUN, PROFILE_DATABASE_PATH, TESTNET_TASKS_DATAFILES
from tools.tools import get_all_tasks


def get_profiles_to_run(cycle: int, profiles: list[Profile]) -> list[Profile]:
    # GETTING PROFILE BATCH TO RUN
    profiles_to_run = []

    # RUN FROM SCRATCH
    if cycle == 1 and CONTINUE_RUN is False:
        for profile in profiles[:PROFILES_TO_RUN]:
            profiles_to_run.append(profile)
    
    # CONTINUE PREVIOUS RUN 
    else:
        for profile in profiles:
            if len(profiles_to_run) < PROFILES_TO_RUN:
                for key in profile.task_results:
                    if profile.task_results[key] is False:
                        profiles_to_run.append(profile)
                        break

    return profiles_to_run


def initialize_profiles() -> (list[Profile], list[Profile]):
    """
    Function to initialize profiles from CSV-tables (profile table and task tables)

    :return: original list of profiles (in order as in CSV), shuffled list of profiles
    """

    ads_profiles = create_profiles_from_csv(PROFILE_DATABASE_PATH)
    shuffled_profiles = ads_profiles.copy()
    shuffle(shuffled_profiles)

    # FILLING PROFILES WITH DATA FROM TASK CSV-TABLES
    for ads_profile in shuffled_profiles:
        for testnet in TESTNET_TASKS_DATAFILES:
            csv_file = TESTNET_TASKS_DATAFILES[testnet]
            update_profile_from_csv(ads_profile, csv_file, testnet)

    return ads_profiles, shuffled_profiles


def create_profiles_from_csv(csv_file_path) -> list[Profile]:
    # CREATING Profile class INSTANCES FROM CSV TABLE

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
    all_tasks = get_all_tasks()
    
    with open(csv_file_path, newline='') as csvfile:
        csvreader = csv.DictReader(csvfile)

        for row in csvreader:
            if row['PROFILE_ID'] == profile.profile_id:
                for key, value in row.items():
                    if key == 'PROFILE_ID':
                        continue  # SKIP PROFILE_ID COLUMN

                    # SKIP TASKS THAT ARE NOT IN CONFIG FILE
                    if f"{testnet} {key}" in all_tasks:
                        if value == 'False':
                            value = False
                        else:
                            value = True

                        dict_key = f"{testnet} {key}"
                        profile.set_task_result(dict_key, value)
                break
