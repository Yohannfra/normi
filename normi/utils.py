#!/usr/bin/python3

import os
import sys

class Utils:

    @classmethod
    def get_file_content(self, fp):
        """ open a file and return its content """
        if os.path.exists(fp):
            if not os.access(fp, os.R_OK):
                sys.exit(f"{fp} : is not readable")
            elif os.path.isdir(fp):
                sys.exit(f"{fp} : is a directory")
        else:
            sys.exit(f"{fp} : file not found")
        try:
            f = open(fp, 'r')
            fc = f.read()
            f.close()
        except:
            sys.exit(f"{fp} : could not open and read file")
        return fc
