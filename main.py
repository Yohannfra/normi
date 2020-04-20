#!/usr/bin/python3

import os
from termcolor import colored
import re
import sys


from normi.list_files import list_files

def main():
    file_list = list_files().walk(sys.argv)
    print(file_list)

if __name__ == '__main__':
    main()
