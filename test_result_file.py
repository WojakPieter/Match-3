from ..save_and_read_to_yml import find_max_result
from io import StringIO


def test_find_max_result(monkeypatch):
    def return_io(name):
        io_dict = "Jan: 3400\nMarek: 3600\nKasia: 2600\n"
        io = StringIO(io_dict)
        return io
    monkeypatch.setattr('save_and_read_to_yml.open_file_to_read', return_io)
    assert find_max_result() == '3600'


def test_find_max_result_from_empty_file(monkeypatch):
    def return_io(name):
        io_dict = ""
        io = StringIO(io_dict)
        return io
    monkeypatch.setattr('save_and_read_to_yml.open_file_to_read', return_io)
    assert find_max_result() == '0'
