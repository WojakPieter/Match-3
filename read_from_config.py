import json


name_of_config_file = 'config.json'


class NoConfigFileError(Exception):
    def __init__(self):
        super().__init__('There is no config file in root directory')


class MalformedJSONDataError(Exception):
    def __init__(self):
        super().__init__('The data in config file is incomplete')


class TooFewColorsError(Exception):
    def __init__(self):
        super().__init__('There must be at least 13 possible colors in config file')


class InvalidSizeError(Exception):
    def __init__(self):
        super().__init__('Board size must be an integer from 5 to 12')


def open_config_file(file_handler):
    try:
        data = json.load(file_handler)
    except FileNotFoundError:
        raise NoConfigFileError
    try:
        colors = data['squares_color']
        mark = data['mark_color']
        size = data['board_size']
    except KeyError:
        raise MalformedJSONDataError
    return data


def read_colors_from_json(file_handler):
    data = open_config_file(file_handler)
    colors = data['squares_color']
    for color in colors:
        while colors.count(color) > 1:
            colors.remove(color)
    if len(colors) < 13:
        raise TooFewColorsError
    return colors


def read_mark_color_from_json(file_handler):
    data = open_config_file(file_handler)
    mark_color = data['mark_color']

    return mark_color


def read_board_size_from_json(file_handler):
    data = open_config_file(file_handler)
    board_size = data['board_size']
    if not isinstance(board_size, int) or not (4 < board_size < 13):
        raise InvalidSizeError
    return board_size
