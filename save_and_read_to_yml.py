import yaml


name_of_result_file = 'result.yml'


def save_result_to_file(name, points):
    file = open(name_of_result_file, 'a')
    yaml.dump({name: points}, file)
    exit(0)


def find_max_result():
    try:
        file = open(name_of_result_file, 'r')
        max_result = 0
        for line in file:
            if line.strip() != '':
                result = line.split(': ')
                max_result = max(max_result, int(result[1]))
        return str(max_result)
    except FileNotFoundError:
        return '0'
