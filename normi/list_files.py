#!/usr/bin/python3

import os
import sys

BUILD_FILES = ['Makefile', 'makefile']

class list_files():
    def __init__(self):
        self. file_list = {'headers': [], 'source': [], 'build': [], 'dir': []}

    def __add_file_to_list(self, filename, dirname=""):
        if os.path.isdir(os.path.join(dirname, filename)):
            self.file_list['dir'].append(os.path.join(dirname, filename))
        if filename.endswith(".c") and filename[0] != '.':
            self.file_list['source'].append(os.path.join(dirname, filename))
        elif filename.endswith(".h") and filename[0] != '.':
            self.file_list['headers'].append(os.path.join(dirname, filename))
        elif filename in BUILD_FILES:
            self.file_list['build'].append(os.path.join(dirname, filename))

    def __check_folder(self, folder):
        for dirname, dirnames, filenames in os.walk(folder):
            for filename in filenames:
                self.__add_file_to_list(filename, dirname)
            if '.git' in dirnames:
                dirnames.remove('.git')

    def __check_errors(self):
        if self.file_list['source'] == [] and self.file_list['headers'] == [] \
                and self.file_list['build'] == []:
            sys.exit("No file to check found")

    def walk(self, argv):
        if len(argv) > 1:
            for args in argv:
                if args != argv[0]:
                    self.__add_file_to_list(args)
            for folder in self.file_list['dir']:
                self.__check_folder(folder)
        else:
            self.__check_folder(".")
        self.__check_errors()
        return self.file_list
