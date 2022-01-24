import yaml


name_of_result_file = 'result.yml'


def open_file_to_read(name):
    return open(name, 'r')


def open_file_to_save(name):
    return open(name, 'a')


def save_result_to_file(name, points):
    '''
        Opens result yaml file and saves name of player and his points. Terminates a program afterwards.
    '''
    file = open_file_to_save(name_of_result_file)
    yaml.dump({name: points}, file)
    file.close()
    exit(0)


def find_max_result():
    '''
        Opens result yaml file and reads the best result.

        Returns:
            int: the maximum value from file, if the file does not exist, returns 0
    '''
    try:
        file = open_file_to_read(name_of_result_file)
        max_result = 0
        for line in file:
            if line.strip() != '':
                result = line.split(': ')
                max_result = max(max_result, int(result[1]))
        return str(max_result)
    except FileNotFoundError:
        return '0'
