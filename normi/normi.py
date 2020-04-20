#!/usr/bin/python3

from .list_files import list_files
from .error_printing import Error_printer

from .checkers.header_checker import Header_checker
from .checkers.source_checker import Source_checker
from .checkers.makefile_checker import Makefile_checker

class Normi:
    def __init__(self, argv):
        self.file_list = list_files().walk(argv)
        self.error_printer = Error_printer()

    def start(self):
        print('ok')
        pass
