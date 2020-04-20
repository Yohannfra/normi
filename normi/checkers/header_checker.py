#!/usr/bin/env python3

from ..utils import Utils

class Header_checker:
    def __init__(self, config, error_printer):
        self.config = config
        self.error_printer = error_printer

    def reset_vars(self):
        pass

    def checkline(self, file_content, line_nb):
        pass

    def run(self, file_list):
        for self.filename in file_list:
            self.reset_vars()
            file_content = Utils.get_file_content(self.filename).split('\n')
            for line_nb in range(len(file_content)):
                self.checkline(file_content, line_nb)
