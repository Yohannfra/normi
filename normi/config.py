#!/usr/bin/python3

import os
import sys

class Config:
    def __init__(self, config_files):
        pass

    @classmethod
    def init_config(self):
        filename = ".normi.toml"
        default_file_content = [
            "hello = 12\n",
        ]
        if os.path.exists(filename):
            sys.exit(f"{filename} already exists, can't init the file")
        try:
            f = open(filename, 'w')
        except:
            sys.exit(f"Could not create file {filename}")
        for line in default_file_content:
            f.write(line)
        f.close()
        print(f"Initialized {filename} with success")
