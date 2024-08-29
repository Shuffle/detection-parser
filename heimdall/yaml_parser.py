# write a simple parser to parse files like rules/impersonation_of_twitter.yaml
# and return a dictionary with the parsed data

import yaml
import os

def parse_yaml_file(file_path):
    with open(file_path, 'r') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    return data

def parse_yaml_files_in_directory(directory):
    data = {}
    for file in os.listdir(directory):
        if file.endswith('.yaml'):
            data[file] = parse_yaml_file(os.path.join(directory, file))
    return data
