#!/usr/bin/python3

import os
from termcolor import colored
import re
import sys
from normi.normi import Normi

def main():
    checker = Normi(sys.argv)
    checker.start()

if __name__ == '__main__':
    main()
