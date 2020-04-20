#!/usr/bin/env python3

from termcolor import colored
from .constants import MAJOR, MINOR

class Error_printer:
    def __init__(self):
        self.minor_err_count = 0
        self.major_err_count = 0
        self.makefile_errors = []
        self.source_errors = []
        self.headers_errors = []

    def add_error(self, path, type, severity, line, message):
        if type == "makefile":
            self.makefile_errors.append({'path' : path, 'line' : line,
                                'message' : message, 'severity' : severity})
        if type == "source":
            self.source_errors.append({'path' : path, 'line' : line,
                                'message' : message, 'severity' : severity})
        if type == "header":
            self.headers_errors.append({'path' : path, 'line' : line,
                                'message' : message, 'severity' : severity})
        if severity == MAJOR:
            self.major_err_count += 1
        elif severity == MINOR:
            self.minor_err_count += 1

    def __print_summary(self):
        print("\nSummary:")
        print(f"\t{colored('minor', 'yellow')} errors : {self.minor_err_count}")
        print(f"\t{colored('major', 'red')} errors : {self.major_err_count}")

    def __print_formated_errors(self, errors):
        last_file = errors[0]['path']

        for e in self.source_errors:
            if last_file != e['path']:
                print("")
            if e['severity'] == MAJOR:
                print(colored(e['path'], 'red'), end=" : ")
            elif e['severity'] == MINOR:
                print(colored(e['path'], 'yellow'), end=" : ")
            print(f"Line {e['line']} : {e['message']}")
            last_file = e['path']

    def print_errors(self):
        if self.makefile_errors != []:
            self.__print_formated_errors(self.makefile_errors)
        if self.headers_errors != []:
            self.__print_formated_errors(self.headers_errors)
        if self.source_errors != []:
            self.__print_formated_errors(self.source_errors)
        self.__print_summary()
