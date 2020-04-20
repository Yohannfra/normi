#!/usr/bin/env python3

from ..utils import Utils
from ..constants import MAJOR, MINOR

class Source_checker:
    def __init__(self, config, error_printer):
        self.config = config
        self.error_printer = error_printer

    def __add_error(self, line, message, severity):
        self.error_printer.add_error(self.filename, "source",
                                     severity, line + 1, message)

    def reset_vars(self):
        pass

    def checkline(self, file_content, line_nb):
        pass

    def check_epitech_header(self, file_content):
        header = ["/*", "** EPITECH PROJECT, ", "** ",
                  "** File description:", "** ", "*/"]
        i = 0
        for line in header:
            if line != file_content[i][0:len(line)]:
                self.__add_error(i, "Invalid or missing epitech header", MAJOR)
            i += 1

    def run(self, file_list):
        for self.filename in file_list:
            self.reset_vars()
            file_content = Utils.get_file_content(self.filename).split('\n')
            self.check_epitech_header(file_content);
            for line_nb in range(len(file_content)):
                self.checkline(file_content, line_nb)
