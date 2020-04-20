#!/usr/bin/python3

class Header_checker:
    def __init__(self, config, error_printer):
        self.config = config
        self.error_printer = error_printer

    def run(self, file_list):
        print(file_list)
