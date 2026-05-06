# This Python file uses the following encoding: utf-8
import sys
from datetime import datetime

class logger:
    def __init__(self, loglevel):
        self.loglevel = loglevel

    COLORS = {
        "DEBUG": "\033[36m",   # голубой
        "INFO": "\033[32m",    # зелёный
        "WARN": "\033[33m",    # жёлтый
        "ERROR": "\033[31m",   # красный
        "RESET": "\033[0m"
    }

    def _print_colored(self, level, module, string, file):
        color = self.COLORS.get(level, "")
        msg = self._format(level, module, string)
        print(f"{color}{msg}{self.COLORS['RESET']}", file=file)

    def _format(self, level, module, string):
        time_str = datetime.now().strftime("%H:%M:%S")
        mod_str = f"|{module}" if module else ""
        return f"[{time_str}] [{level}{mod_str}] {string}"

    def error(self, string, module = ''):
        if self.loglevel >= 1:
            self._print_colored("ERROR", module, string, file=sys.stderr)

    def warn(self, string, module = ''):
        if self.loglevel >= 2:
            self._print_colored("WARN", module, string, file=sys.stdout)

    def log(self, string, module = ''):
        if self.loglevel >= 3:
            self._print_colored("INFO", module, string, file=sys.stdout)

    def debug(self, string, module = ''):
        if self.loglevel >= 4:
            self._print_colored("DEBUG", module, string, file=sys.stdout)

console = logger(3)