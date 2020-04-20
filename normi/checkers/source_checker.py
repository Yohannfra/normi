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
        self.nb_functions = 0
        self.line_is_declaration = False
        self.first_line_of_function = 0

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

    def __check_trailing_whitespaces(self, fc, line_nb):
        if re.findall(r"[ \t]$", fc[line_nb]):
            self.__add_error(line_nb, "Trailing whitespace", MINOR)

    def __check_space_after_comma(self, fc, line_nb):
        pattern = re.findall(r",\S", fc[line_nb])
        if len(pattern) > 0 and not Utils.check_if_is_text(pattern, fc[line_nb]):
            self.__add_error(line_nb, "No space after comma", MINOR)

    def __check_space_after_keyword(self, fc, line_nb):
        keywords = ["while", "for", "if", "else if", "return", "switch"]
        for k in keywords:
            if re.findall(rf"^[ \t]*{k}\(", fc[line_nb]):
                self.__add_error(line_nb, f"No space after {k}", MINOR)

    def __is_function_declaration(self, line):
        return re.findall(r"^[a-zA-Z_]+ [a-zA-Z_]*\(.*\)$", line)

    def __check_function_lines(self, fc, line_nb):

        if self.__is_function_declaration(fc[line_nb]) and \
                fc[line_nb + 1] == "{":
            self.nb_functions += 1
            self.first_line_of_function = line_nb + 3
        elif fc[line_nb] == "}" and self.first_line_of_function > 0:
            if line_nb - self.first_line_of_function + 1 > \
                                        self.config.get('max_size_function'):
                name = fc[self.first_line_of_function - 3].\
                                                split(' ')[1:][0].split('(')[0]
                self.__add_error(line_nb, f"The function {name} has "
                    f"{line_nb - self.first_line_of_function + 1} lines", MAJOR)
            self.first_line_of_function = -1

    def __checkline(self, fc, line_nb):
        self.__check_trailing_whitespaces(fc, line_nb)
        self.__check_space_after_comma(fc, line_nb)
        self.__check_space_after_keyword(fc, line_nb)
        self.__check_function_lines(fc, line_nb)

    def run(self, file_list):
        for self.filename in file_list:
            self.__reset_vars()
            fc = Utils.get_file_content(self.filename).split('\n')
            if self.config.get('epitech_header') == True:
                self.__check_epitech_header(fc)
            for line_nb in range(len(fc)):
                self.__checkline(fc, line_nb)
            self.__check_empty_last_line(fc)
