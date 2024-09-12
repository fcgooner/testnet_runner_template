from config import TESTNET_TASKS


def get_all_tasks() -> list[str]:
    all_tasks = []
    for testnet in TESTNET_TASKS:
        for task in TESTNET_TASKS[testnet]['CORE']:
            all_tasks.append(task)

        for task in TESTNET_TASKS[testnet]['OPTIONAL']:
            all_tasks.append(task)

        for task in TESTNET_TASKS[testnet]['GROUP']:
            all_tasks.append(task)

    return all_tasks
