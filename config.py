# ANTIDETECT BROWSER SETTINGS
ANTIC_PORT = "50325"            # API -> API Settings -> Connection (http://local.adspower.net:ПОРТ)

# COMMON SETTINGS
CONTINUE_RUN = False            # if True - don't reset task results from previous runs.
                                # Useful if previous run failed for some reason
                                # or if you want rerun only failed tasks

LOG_LEVEL = "DEBUG"             # Logging level

PROFILE_DATABASE_PATH = 'data/profile_database.csv'     # Path to CSV-table with profiles
PROFILES_TO_RUN = 5                                     # Number of profiles to run simultaniously
MAX_TASK_ATTEMPTS = 1                                   # Number of script runs (1 run = all profiles)
MAX_WALLET_RETRIES = 5  # Number of attemps when looking for wallet extension window during interaction (connecct, sign etc)

WALLET_NAMES = [        # List of wallets to unlock before executing tasks
    'RABBY',            # Note: in this version of template only Rabby Wallet unlocking is implemented
]


# TESTNET SETTINGS

TESTNET_TASKS_DATAFILES = {             # Path to testnet tasks CSV-table
    "TESTNET 1": "testnets/first_testnet/testnet_data/testnet1_tasks_data.csv",
    "TESTNET 2": "testnets/second_testnet/testnet_data/testnet2_tasks_data.csv",
}

CRITICAL_TASKS = ["TESTNET1 TASK1"]     # List of tasks, without the successful completion of which there is no point
                                        # in performing other tasks
                                        # For example, login to testnet website. No point trying to perworm, let's say, swap,
                                        # when you weren't able to log in.

TESTNET_TASKS = {

    # TESTNET 1
    "TESTNET 1": {
        'CORE': [               # Tasks, that are executed first, execution order not shuffled
            "TESTNET1 TASK1",
        ],
        'OPTIONAL': [           # Tasks, that are executed after CORE tasks, execution order is shuffled
            "TESTNET1 TASK2",
            "TESTNET1 TASK3",
        ],
        'GROUP': [              # Tasks, that inserted at random place inside OPTIONAL tasks list, order shuffled
            "TESTNET1 TASK4",   # For example: [task4, task5], task2, task3
            "TESTNET1 TASK5"    # or: task3, [task4, task5], task2
        ]
    },

    # TESTNET 2
    "TESTNET 2": {
        'CORE': [
                "TESTNET2 TASK1",
                "TESTNET2 TASK2"
        ],
        'OPTIONAL': [
                "TESTNET2 TASK3"
        ],
        'GROUP': []
    }
}
