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
            print(f"{fp} : file not found")
            return None
        try:
            f = open(fp, 'r')
            fc = f.read()
            f.close()
        except:
            print(f"{fp} : could not open and read file")
            return None
        return fc

    @classmethod
    def check_if_is_text(self, pattern, line):
        is_str = [False, False]
        index = line.find(pattern[0])
        i = 0

        for char in line:
            if char == "'":
                is_str[0] = not is_str[0]
            if char == '"':
                is_str[1] = not is_str[1]
            if i == index:
                if is_str[0] or is_str[1]:
                    if len(pattern) > 1:
                        pattern.remove(pattern[0])
                        return self.check_if_is_text(pattern, line)
                    else:
                        return True
                else:
                    return False
            i += 1
        return False
