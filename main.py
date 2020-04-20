#!/usr/bin/python3

import sys
from normi.normi import Normi
from normi.config import Config

def main():
    if len(sys.argv) == 2 and sys.argv[1] == "init":
        Config.init_config()
    else:
        checker = Normi(sys.argv)
        checker.start()

if __name__ == '__main__':
    main()
