# Common info
This template is mostly focused on interacting with testnet websites using playwright library, and writen with AdsPower and Rabby Wallet in mind.

If you use other antidetect browser - change logic behind launching and closing profiles in tools/browser_launcher.py

You can also use this template to execute blockchain tasks directly using web3 library, though you need to rewrite logic in run_testnets.py, because now it launches profiles regardless whether it's a website task or blockchain one.

# config.py
This file contains configurable variables, like testnet list, task list, antidetect browser port etc.

# CSV Data tables
## data/profile_database.csv
Stores data about profiles. Need to be filled manually.

You can add as many new colums as you like, just don't forget to update `create_profiles_from_csv()` function in **tools/profile_handler.py** and `__init__` method in Profile class (**classes/ads_profile.py**)

## testnets/[testnet_name]/testnet_data/[testnet_name]_tasks_data.csv
Stores data with profile task results.

Task results reset to `False` every script run, unless `CONTINUE_RUN` set to `True` in **config.py**

# Variable files
## data/variables.py
This file contains non-configurable variables, either for whole project or common for all testnets (browser exctension urls, color codes etc.)

## testnets/[testnet_name]/testnet_data/[testnet_name]_variables.py
These files contain non-configurable variables for specific testnet (testnet urls etc.)

# IMPORTANT: Task names
Task names in config.py must consist of testnet name and activity name divided by one blank space. For example:\
`MOVEMENT_TESTNET CHECK_IN` - ok\
`MOVEMENT TESTNET CHECK IN` - not ok\

Task names in **[testnet_name]_tasks_data.csv** must consist only from activity name, without testnet name and blank spaces, unlike **config.py**. For example:\
`CHECK_IN` - ok\
`MOVEMENT_TESTNET CHECK_IN` - not ok\

In short, if a task in **config.py** called `MOVEMENT CHECKIN`, in .csv task table it must be called `CHECKIN`

# Logger
This template has 2 loggers:
 * for console output (colorized, without timestamps and log levels)
 * for file output

Every run the script creates a log file with unique name, based on current time.

# Profile class (classes/ads_profile.py)
Class for easy access to profile data (private keys, passwords, task results etc.)\
Class instances created at the start of the script from **data/profile_database.csv** and then updated with testnet task results from **testnets/[testnet_name]/testnet_data/[testnet_name]_tasks_data.csv** files

# Script Flow
1. Reset task csv tables
2. Initialize profiles from csv profile table
3. Gather profiles
4. Get batch of random profiles (repeat until no more profiles left)\
   4.1. Start working with profile\
     &nbsp;&nbsp;&nbsp;4.1.2. Launch runner for random testnet from list (repeat for every testnet)\
     &nbsp;&nbsp;&nbsp;4.1.3. Gather tasks for profile\
     &nbsp;&nbsp;&nbsp;4.1.4. Run all tasks for profile
5. Print results for all profiles

Repeat from STEP 3 if `MAX_TASK_ATTEMPTS > 1`

# Useful tips
## Run script for specific testnet(s)
To run the script only for specific testnet(s), comment out testnets you don't need in `TESTNET_TASKS_DATAFILES` variable in **config.py**

In this example the script will only run tasks for TESTNET 2:
```
TESTNET_TASKS_DATAFILES = {
    # "TESTNET 1": "testnets/first_testnet/testnet_data/testnet1_tasks_data.csv",
    "TESTNET 2": "testnets/second_testnet/testnet_data/testnet2_tasks_data.csv",
}
```
## Run script for specific task(s)
To run the script only for specific task(s), comment out tasks you don't need in `TESTNET_TASKS` variable in **config.py**

In this example the script will only run `TESTNET1 TASK2` and `TESTNET2 TASK1`:
```
TESTNET_TASKS = {
    "TESTNET 1": {
        'CORE': [               
            # "TESTNET1 TASK1",
        ],
        'OPTIONAL': [
            "TESTNET1 TASK2",
            # "TESTNET1 TASK3",
        ],
        'GROUP': [
            # "TESTNET1 TASK4",
            # "TESTNET1 TASK5"
        ]
    },
    # TESTNET 2
    "TESTNET 2": {
        'CORE': [
                "TESTNET2 TASK1",
                # "TESTNET2 TASK2"
        ],
        'OPTIONAL': [
                # "TESTNET2 TASK3"
        ],
        'GROUP': []
    }
}
```

## Run script for specific profile(s)
To run the script only for specific profile(s), remove profiles you don't need from **data/profile_database.csv**

In this example the script will run only profile 3 (qwerty3):
```
PROFILE_NUMBER,PROFILE_ID,WALLET_PASS,PK
3,qwerty3,superpassword,0x0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c
```

## Final tip
You can combine all previous tips to run the script for specific profile(s), specific testnet(s) and specific task(s)
