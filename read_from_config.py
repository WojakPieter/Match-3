import json


name_of_config_file = 'config.json'


def open_config_file(file_handler):
    data = json.load(file_handler)
    return data


def read_colors_from_json(file_handler):
    data = open_config_file(file_handler)
    colors = data['squares_color']
    return colors


def read_mark_color_from_json(file_handler):
    data = open_config_file(file_handler)
    mark_color = data['mark_color']
    return mark_color


def read_board_size_from_json(file_handler):
    data = open_config_file(file_handler)
    board_size = data['board_size']
    return board_size


