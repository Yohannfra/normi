#!/usr/bin/env python3

from ..utils import Utils
from ..constants import MAJOR, MINOR
import re

class Source_checker:
    def __init__(self, config, error_printer):
        self.config = config
        self.error_printer = error_printer

    def __add_error(self, line, message, severity):
        self.error_printer.add_error(self.filename, "source",
                                     severity, line + 1, message)

    def __reset_vars(self):
        pass

    def __check_trailing_whitespaces(self, fc, line_nb):
        if re.findall(r"[ \t]$", fc[line_nb]):
            self.__add_error(line_nb, "Trailing whitespace", MINOR)

    def __check_epitech_header(self, fc):
        header = ["/*", "** EPITECH PROJECT, ", "** ",
                  "** File description:", "** ", "*/"]
        i = 0
        for line in header:
            if line != fc[i][0:len(line)]:
                self.__add_error(i, "Invalid or missing epitech header", MAJOR)
            i += 1

    def __check_empty_last_line(self, fc):
        last = len(fc) - 1
        if last > 1 and fc[last] == "" and fc[last - 1] == "":
            self.__add_error(last - 1, "Last line of the file is empty", MAJOR)

    def __check_space_after_comma(self, fc, line_nb):
        pattern = re.findall(r",\S", fc[line_nb])
        if len(pattern) > 0 and not Utils.check_if_is_text(pattern, fc[line_nb]):
            self.__add_error(line_nb, "No space after comma", MINOR)

    def __checkline(self, fc, line_nb):
        self.__check_trailing_whitespaces(fc, line_nb)
        self.__check_space_after_comma(fc, line_nb);

    def run(self, file_list):
        for self.filename in file_list:
            self.__reset_vars()
            fc = Utils.get_file_content(self.filename).split('\n')
            if self.config.get('epitech_header') == True:
                self.__check_epitech_header(fc)
            for line_nb in range(len(fc)):
                self.__checkline(fc, line_nb)
            self.__check_empty_last_line(fc)
