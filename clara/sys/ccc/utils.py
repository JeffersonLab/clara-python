# coding=utf-8


def remove_first(input_string, first_character):
    if input_string.startswith(first_character):
        return input_string[1:]
    else:
        return input_string
