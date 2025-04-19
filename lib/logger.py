RED = '\033[31m'
GREEN = '\033[32m'
RESET = '\033[0m'

def info(message):
    print(f"[{GREEN}+{RESET}] {message}")

def error(message):
    print(f"[{RED}-{RESET}] {message}")