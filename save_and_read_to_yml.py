import yaml


name_of_result_file = 'result.yml'


def save_result_to_file(name, points):
    '''
        Opens result yaml file and saves name of player and his points. Terminates a program afterwards.
    '''
    file = open(name_of_result_file, 'a')
    yaml.dump({name: points}, file)
    exit(0)


def find_max_result():
    '''
        Opens result yaml file and reads the best result.

        Returns:
            int: the maximum value from file, if the file does not exist, returns 0
    '''
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
