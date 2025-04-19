from io import StringIO
from read_from_config import *
import pytest


def test_read_data():
    config_file_dict = {
                  "squares_color": ["red", "yellowgreen", "green", "gold", "black",
                                    "purple", "maroon", "salmon", "springgreen", "magenta", "cyan", "gray", "lightseagreen"],
                  "mark_color": "blue",
                  "board_size": 6
                  }
    io = StringIO(json.dumps(config_file_dict))
    assert read_colors_from_json(io) == ["red", "yellowgreen", "green", "gold", "black",
                                         "purple", "maroon", "salmon", "springgreen", "magenta", "cyan",
                                         "gray", "lightseagreen"]
    io = StringIO(json.dumps(config_file_dict))
    assert read_board_size_from_json(io) == 6
    io = StringIO(json.dumps(config_file_dict))
    assert read_mark_color_from_json(io) == 'blue'


def test_find_colors_too_few():
    config_file_dict = {
                  "squares_color": ["red", "yellowgreen", "green", "gold", "black",
                                    "purple", "maroon", "salmon", "springgreen", "magenta", "cyan"],
                  "mark_color": "blue",
                  "board_size": 6
                  }

    io = StringIO(json.dumps(config_file_dict))
    with pytest.raises(TooFewColorsError):
        read_colors_from_json(io)


def test_reapating_colors_too_few():
    config_file_dict = {
                  "squares_color": ["red", "yellowgreen", "green", "gold", "black",
                                    "purple", "maroon", "salmon", "cyan", "cyan", "cyan", "cyan", "cyan"],
                  "mark_color": "blue",
                  "board_size": 6
                  }
    io = StringIO(json.dumps(config_file_dict))
    with pytest.raises(TooFewColorsError):
        read_colors_from_json(io)


def test_malformed_config_data():
    config_file_dict = {
                  "mark_color": "blue",
                  "board_size": 6
                  }
    io = StringIO(json.dumps(config_file_dict))
    with pytest.raises(MalformedJSONDataError):
        read_colors_from_json(io)
    io = StringIO(json.dumps(config_file_dict))
    with pytest.raises(MalformedJSONDataError):
        read_board_size_from_json(io)


def test_wrong_size():
    config_file_dict = {
                  "squares_color": ["red", "yellowgreen", "green", "gold", "black",
                                    "purple", "maroon", "salmon", "springgreen", "magenta", "cyan", "gray", "lightseagreen"],
                  "mark_color": "blue",
                  "board_size": 15
                  }
    io = StringIO(json.dumps(config_file_dict))
    with pytest.raises(InvalidSizeError):
        read_board_size_from_json(io)

    config_file_dict = {
                  "squares_color": ["red", "yellowgreen", "green", "gold", "black",
                                    "purple", "maroon", "salmon", "springgreen", "magenta", "cyan", "gray", "lightseagreen"],
                  "mark_color": "blue",
                  "board_size": 3
                  }
    io = StringIO(json.dumps(config_file_dict))
    with pytest.raises(InvalidSizeError):
        read_board_size_from_json(io)
