#!/usr/bin/env python3

from ..utils import Utils
from ..constants import MAJOR, MINOR, C_TYPES
import re
import os

class Source_checker:
    def __init__(self, config, error_printer):
        global C_TYPES

        self.config = config
        self.error_printer = error_printer
        C_TYPES = C_TYPES + self.config.get("additionnal_types")

    def __add_error(self, line, message, severity):
        self.error_printer.add_error(self.filename, "source",
                                     severity, line + 1, message)

    def __reset_vars(self):
        self.nb_functions = 0
        self.line_is_declaration = False
        self.first_line_of_function = 0
        self.is_a_comment = False

    def __check_epitech_header(self, fc):
        header = ["/*", "** EPITECH PROJECT, ", "** ",
                  "** File description:", "** ", "*/"]
        i = 0
        for line in header:
            if line != fc[i][0:len(line)]:
                self.__add_error(i, "Invalid or missing epitech header", MAJOR)
            i += 1

    def __check_empty_last_line(self, fc):
        last = len(fc) - 1
        if last > 1 and fc[last] == "" and fc[last - 1] == "":
            self.__add_error(last - 1, "Last line of the file is empty", MAJOR)

    def __check_trailing_whitespaces(self, fc, line_nb):
        if re.findall(r"[ \t]$", fc[line_nb]):
            self.__add_error(line_nb, "Trailing whitespace", MINOR)

    def __check_space_after_comma(self, fc, line_nb):
        pattern = re.findall(r",\S", fc[line_nb])
        if len(pattern) > 0 and not Utils.check_if_is_text(pattern, fc[line_nb]):
            self.__add_error(line_nb, "No space after comma", MINOR)

    def __check_space_after_keyword(self, fc, line_nb):
        keywords = ["while", "for", "if", "else if", "return", "switch"]
        for k in keywords:
            if re.findall(rf"^[ \t]*{k}\(", fc[line_nb]):
                self.__add_error(line_nb, f"No space after {k}", MINOR)

    def __is_function_declaration(self, line):
        return re.findall(r"^[a-zA-Z_]+ [a-zA-Z_]*\(.*\)$", line)

    def __check_function_lines(self, fc, line_nb):
        # TODO FIX FOR MULTI LINE DECLARATIONS
        if self.__is_function_declaration(fc[line_nb]) and \
                fc[line_nb + 1] == "{":
            self.nb_functions += 1
            self.first_line_of_function = line_nb + 3
        elif fc[line_nb] == "}" and self.first_line_of_function > 0:
            if line_nb - self.first_line_of_function + 1 > \
                                        self.config.get('max_size_function'):
                name = fc[self.first_line_of_function - 3].\
                                                split(' ')[1:][0].split('(')[0]
                self.__add_error(line_nb, f"The function {name} has "
                    f"{line_nb - self.first_line_of_function + 1} lines", MAJOR)
            self.first_line_of_function = -1

    def __check_len_line(self, fc, line_nb):
        l = len(fc[line_nb])
        if l > self.config.get('max_len_line'):
            self.__add_error(line_nb, f"Too long line : {l}", MAJOR)

    def __check_empty_parenthese(self, fc, line_nb):
        if re.findall(r"^[a-zA-Z_]+ [a-zA-Z_]*\([ \t]*\)$", fc[line_nb]) and \
            self.config.get('requiere_void_when_no_args'):
                self.__add_error(line_nb, f"This function should take "\
                                 "'void' as argument", MINOR)

    def __check_too_many_parameters(self, fc, line_nb):
        if self.__is_function_declaration(fc[line_nb]):
            count = fc[line_nb].count(',')
            if count > self.config.get('max_parameters_to_functions') - 1:
                self.__add_error(line_nb, "This function takes more than "\
                    f"{count} parameters", MAJOR)

    def __check_return_value_in_parenthese(self, fc, line_nb):
        if not self.config.get('return_values_in_parenthese'):
            return
        if re.findall(r"^[ ]{4,}return[^a-zA-Z_]", fc[line_nb]) and \
            re.findall(r"^[ ]{4,}return[^;]", fc[line_nb]):
            if not (re.findall(r"^[ ]{4,}return \(", fc[line_nb])):
                self.__add_error(line_nb, "Return value must be in parenthese", MINOR)

    def __check_if_line_is_declaration(self, fc, line_nb):
        global C_TYPES

        last_line_is_declaration = self.line_is_declaration
        for t in C_TYPES:
            if re.findall(rf"^[ \t]+{t} ", fc[line_nb]):
                self.line_is_declaration = True
                return
        self.line_is_declaration = False
        if not self.line_is_declaration and last_line_is_declaration:
            if fc[line_nb] == "":
                pass
            elif line_nb > 0 and not re.findall(r";$", fc[line_nb - 1]):
                self.line_is_declaration = True
            else:
                self.__add_error(line_nb,
                                 "Line is not empty after declarations", MINOR)
        if not self.line_is_declaration and not last_line_is_declaration:
            if fc[line_nb] == "" and self.first_line_of_function > 0:
                self.__add_error(line_nb,"Empty line", MINOR)

    def __check_multiple_empty_lines(self, fc, line_nb):
        if fc[line_nb] == "" and self.first_line_of_function < 1:
            if line_nb < len(fc) - 1 and fc[line_nb + 1] == "" and \
                    line_nb > 0 and fc[line_nb - 1] != "":
                self.__add_error(line_nb,"Too many empty lines", MINOR)

    def __check_misplaced_space(self, fc, line_nb):
        if re.findall(" ;$", fc[line_nb]):
                self.__add_error(line_nb,"Misplaced space before ';'", MINOR)

        double_spaces = re.findall(r"  ", fc[line_nb].lstrip())
        if double_spaces and not Utils.check_if_is_text(double_spaces,
                                                        fc[line_nb].lstrip()):
            self.__add_error(line_nb,"Double space detected", MINOR)

        space_before_coma = re.findall(r" ,", fc[line_nb])
        if space_before_coma and \
                not Utils.check_if_is_text(space_before_coma, fc[line_nb]):
            self.__add_error(line_nb,"Misplaced space before ','", MINOR)

    def __check_space_before_curly_bracket(self, fc, line_nb):
        if re.findall(r"[^ ]\{[ ]*$", fc[line_nb]):
            self.__add_error(line_nb,
                             "Missing space before curly bracket", MINOR)

    def __check_unicode_caracters(self, fc, line_nb):
        if not fc[line_nb].isascii():
            self.__add_error(line_nb, "Non ascii caracters detected", MINOR)

    # Thanks to https://github.com/ronanboiteau/NormEZ for those regexes
    def __check_operators_spaces(self, fc, line_nb):
        regex_dict = {
            '=' : r"[^\t&|=^><+\-*%\/! ]=[^=]|[^&|=^><+\-*%\/!]=[^= \n]",
            '==': r"[^\t ]==|==[^ \n]",
            '!=': r"[^\t ]!=|!=[^ \n]",
            '<=': r"[^\t <]<=|[^<]<=[^ \n]",
            '>=': r"[^\t >]>=|[^>]>=[^ \n]",
            '&&': r"[^\t ]&&|&&[^ \n]",
            '||': r"[^\t ]\|\||\|\|[^ \n]",
            '+=': r"[^\t ]\+=|\+=[^ \n]",
            '-=': r"[^\t ]-=|-=[^ \n]",
            '*=': r"[^\t ]\*=|\*=[^ \n]",
            '/=': r"[^\t ]\/=|\/=[^ \n]",
            '%=': r"[^\t ]%=|%=[^ \n]",
            '^': r"[^\t ]\^|\^[^ =\n]",
            '>>': r"[^\t ]>>[^=]|>>[^ =\n]",
            '<<': r"[^\t ]<<[^=]|<<[^ =\n]",
            '>>=': r"[^\t ]>>=|>>=[^ \n]",
            '<<=': r"[^\t ]<<=|<<=[^ \n]",
        }
        for k in regex_dict.keys():
            if re.findall(regex_dict[k], fc[line_nb]):
                self.__add_error(line_nb, f"Missing space arround '{k}'", MINOR)


    def __check_bracket_at_end_of_line(self, fc, line_nb):
        if re.findall(r"^[ ]+\{$", fc[line_nb]) and \
                self.config.get('brackets_style') == 'end_of_line':
            self.__add_error(line_nb,
                        "Misplaced bracket at the begining of the line", MINOR)

    def __check_forbidden_functions(self, fc, line_nb):
        forbidden_functions = self.config.get('forbidden_functions')

        for f in forbidden_functions:
            reg = re.escape(str(f)) + r"\("
            reg_not = "my_" + re.escape(str(f))
            if re.findall(reg, fc[line_nb]) and \
                    not re.findall(reg_not, fc[line_nb]):
                self.__add_error(line_nb,
                                 f"Forbidden function detected : '{f}'", MAJOR)

    def __check_misplaced_pointer_symbol(self, fc, line_nb):
        global C_TYPES

        for t in C_TYPES:
            if re.findall(rf"{t}\*", fc[line_nb]):
                self.__add_error(line_nb, "Misplaced pointer symbol", MINOR)

    def __check_indentation(self, fc, line_nb):
        i = 0
        for c in fc[line_nb]:
            if c != ' ':
                break
            i += 1
        if fc[line_nb][i] == '\t' and self.config.get('indent_style') == 'space':
            self.__add_error(line_nb, "Tab detected in indentation", MINOR)
        if i % 4 != 0:
            self.__add_error(line_nb, "Bad indentation level", MINOR)

    def __check_comments(self, fc, line_nb):
        if "//" in fc[line_nb] and not Utils.check_if_is_text("//", fc[line_nb]) \
            or "/*" in fc[line_nb] and not Utils.check_if_is_text("/*", fc[line_nb]):
            if self.first_line_of_function > 0:
                self.__add_error(line_nb,
                                 "Forbiddent comment within a function", MINOR)
        if re.findall(r"^[ \t]*\/\*", fc[line_nb]):
            self.is_a_comment = True
            return 1
        elif re.findall(r"^[ \t]*\/\/", fc[line_nb]):
            return 1
        else:
            if line_nb > 0 and "*/" in fc[line_nb - 1] and not \
                    Utils.check_if_is_text("*/", fc[line_nb - 1]):
                self.is_a_comment = False
                return 0
            return self.is_a_comment

    def __check_deepness(self, fc, line):
        # TODO
        pass

    def __checkline(self, fc, line_nb):
        if self.__check_comments(fc, line_nb):
            return
        self.__check_multiple_empty_lines(fc, line_nb)
        self.__check_if_line_is_declaration(fc, line_nb)
        if fc[line_nb] != "":
            self.__check_too_many_parameters(fc, line_nb)
            self.__check_space_after_keyword(fc, line_nb)
            self.__check_function_lines(fc, line_nb)
            self.__check_trailing_whitespaces(fc, line_nb)
            self.__check_space_after_comma(fc, line_nb)
            self.__check_len_line(fc, line_nb)
            self.__check_empty_parenthese(fc, line_nb)
            self.__check_return_value_in_parenthese(fc, line_nb)
            self.__check_misplaced_space(fc, line_nb)
            self.__check_space_before_curly_bracket(fc, line_nb)
            self.__check_unicode_caracters(fc, line_nb)
            self.__check_operators_spaces(fc, line_nb)
            self.__check_bracket_at_end_of_line(fc, line_nb)
            self.__check_forbidden_functions(fc, line_nb)
            self.__check_misplaced_pointer_symbol(fc, line_nb)
            self.__check_indentation(fc, line_nb)
            self.__check_deepness(fc, line_nb)

    def run(self, file_list):
        for self.filename in file_list:
            self.__reset_vars()
            fc = Utils.get_file_content(self.filename).split('\n')
            if self.config.get('epitech_header') == True:
                self.__check_epitech_header(fc)
            for line_nb in range(len(fc)):
                self.__checkline(fc, line_nb)
            self.__check_empty_last_line(fc)
