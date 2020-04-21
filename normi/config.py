#!/usr/bin/env python3

import os
import sys
import toml
from .utils import Utils

DEFAULT_FILE_CONTENT = [
    "indent_style = 'spaces'",
    "indent_size = 4",
    "max_len_line = 80",
    "max_size_function = 20",
    "max_function_in_file = 5",
    "epitech_header = true",
    "return_values_in_parenthese = true",
    'forbidden_functions = []',
    "forbidden_comments_in_functions = true",
    "space_after_keyword = true",
    "space_after_coma = true",
    "requiere_void_when_no_args = true",
    "max_parameters_to_functions = 4",
    "max_variable_per_function = -1",
    "brackets_style = 'end_of_line'",
    "additionnal_types = []"
]

class Config:
    def __init__(self):
        self.settings = {}
        self.config_file = ".normi.toml"

    def parse_config(self):
        content = Utils.get_file_content(self.config_file)
        if content == None:
            self.settings = toml.loads("\n".join(DEFAULT_FILE_CONTENT))
            print("Using default configuration")
        else:
            self.settings = toml.loads(content)

    @classmethod
    def init_config(self):
        config_file = ".normi.toml"
        if os.path.exists(config_file):
            sys.exit(f"{config_file} already exists, can't init the file")
        try:
            f = open(config_file, 'w')
        except:
            sys.exit(f"Could not create file {config_file}")
        for line in DEFAULT_FILE_CONTENT:
            f.write(line + '\n')
        f.close()
        print(f"Initialized {config_file} with success")

    def get(self, param):
        return self.settings[param]
