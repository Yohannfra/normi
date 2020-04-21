#!/usr/bin/env python3

from .list_files import list_files
from .error_printing import Error_printer
from .config import Config

from .checkers.header_checker import Header_checker
from .checkers.source_checker import Source_checker
from .checkers.makefile_checker import Makefile_checker

from .constants import C_TYPES

class Normi:
    def __init__(self, argv):
        self.file_list = list_files().walk(argv)
        self.error_printer = Error_printer()
        self.config = Config()
        self.config.parse_config()
        self.makefile_checker = Makefile_checker(self.config, self.error_printer)
        self.source_checker = Source_checker(self.config, self.error_printer)
        self.header_checker = Header_checker(self.config, self.error_printer)

    def start(self):
        self.makefile_checker.run(self.file_list['build'])
        self.header_checker.run(self.file_list['headers'])
        self.source_checker.run(self.file_list['source'])
        self.error_printer.print_errors()
