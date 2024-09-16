from loguru import logger

from data.variables import ALL_TASKS, BLUE, RESET


class Profile:
    def __init__(self, profile_number: str, profile_id: str, wallet_pass: str, pk: str):
        self.profile_number = profile_number
        self.profile_id = profile_id
        self.wallet_pass = wallet_pass
        self.pk = pk
        self.task = None
        self.task_results = {}

    def __str__(self) -> str:
        return f"{BLUE}Profile {self.profile_number} ({self.profile_id}):{RESET}\n{self.task_results}\n"

    def set_task_result(self, key, value):
        self.task_results[key] = value

    def get_task_result(self, task):
        return self.task_results.get(task, None)

    def print_task_results(self):
        logger.log("PRINTOUT_BLUE", f"\nPROFILE {self.profile_number} ({self.profile_id})")

        # FINDING MAX LENGTH OF TASK NAMES FOR FORMATTING
        max_task_name_length = max(len(task) for task in self.task_results)

        for task_name, result in self.task_results.items():
            if task_name in ALL_TASKS:
                result_str = "SUCCESS" if result else "FAILED"

                if result:
                    logger.log("PRINTOUT_GREEN", f"    {task_name.ljust(max_task_name_length)}: {result_str}")
                else:
                    logger.log("PRINTOUT_RED", f"    {task_name.ljust(max_task_name_length)}: {result_str}")
