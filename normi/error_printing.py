#!/usr/bin/python3

from termcolor import colored

class Error_printer:
    def __init__(self):
        self.minor_err = 0
        self.major_err = 0
        self.makefile_errors = []
        self.source_errors = []
        self.headers_errors = []

    def add_error(self, type, severity, line, message):
        if type == "makefile":
            self.makefile_errors.append({'severity' : severity, \
                                         'line' : line, 'message' : message})
        if type == "source":
            self.source_errors.append({'severity' : severity, \
                                       'line' : line, 'message' : message})
        if type == "header":
            self.headers_errors.append({'severity' : severity, \
                                        'line' : line, 'message' : message})

    def print_summary(self):
        pass

    def print_errors(self):
        pass
