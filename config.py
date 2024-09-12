# АНТИДЕТЕКТ БРАУЗЕР
ANTIC_PORT = "50325"            # Порт можна подивитися в самому AdsPower через ліву бокову панель:
                                # API -> API Settings -> Connection (http://local.adspower.net:ПОРТ)

# ЗАГАЛЬНІ НАЛАШТУВАННЯ
CONTINUE_RUN = False            # True - Не очищати результати попереднього прогону. Корисно, якщо попередній
                                # прогон перервався з якоїсь причини, або для прогону лише False завдань

LOG_LEVEL = "DEBUG"             # Рівень логування

PROFILE_DATABASE_PATH = 'data/profile_database.csv'     # Шлях до таблиці з профілями
PROFILES_TO_RUN = 5                                     # Кількість профілів, які проганятимуться одночасно
MAX_TASK_ATTEMPTS = 1                                   # Кількість повних прогонів
                                                        # 1 = усі профілі проганятимуться тільки 1 раз
MAX_WALLET_RETRIES = 5      # Кількість спроб пошуку вікна гаманця під час взаємодії (конект, підпис транзакцій тощо)

WALLET_NAMES = [        # Список гаманців, які потрібно розблокувати перед початком виконання завдань
    'RABBY',            # У цій версії реалізовано лише розблокування Rabby
]


# НАЛАШТУВАННЯ ТЕСТНЕТІВ

TESTNET_TASKS_DATAFILES = {             # Шлях до таблиці завдань тестнетів
    "TESTNET 1": "testnets/first_testnet/testnet_data/testnet1_tasks_data.csv",
    "TESTNET 2": "testnets/second_testnet/testnet_data/testnet2_tasks_data.csv",
}

CRITICAL_TASKS = ["TESTNET1 TASK1"]        # Завдання, без успішного виконання яких немає сенсу виконувати інші завдання

TESTNET_TASKS = {

    # TESTNET 1
    "TESTNET 1": {
        'CORE': [               # Завдання, які виконуються в першу чергу, і в тому порядку, як записані
            "TESTNET1 TASK1",
        ],
        'OPTIONAL': [           # Завдання, які виконуються після CORE завдань, порядок перемішується
            "TESTNET1 TASK2",
            "TESTNET1 TASK3",
        ],
        'GROUP': [              # Завдання, які вставляються на випадкове місце поміж OPTIONAL завдань,
            "TESTNET1 TASK4",   # але порядок яких не перемішується, наприклад:
            "TESTNET1 TASK5"    # [task4, task5], task2, task3 або task3, [task4, task5], task2
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
