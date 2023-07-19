import datetime as dt
from colorama import Fore


def log(in_print, status="info") -> None:
    log_time = dt.datetime.now()
    if status == "success":
        print(Fore.GREEN + f'[{status.upper()}][{log_time}]: {in_print} \033[39m')
    elif status == "warning":
        print(Fore.YELLOW + f'[{status.upper()}][{log_time}]: {in_print} \033[39m')
    elif status == "error":
        print(Fore.RED + f'[{status.upper()}][{log_time}]: {in_print} \033[39m')
    else:
        print(f'[{status.upper()}][{log_time}]: {in_print}')
