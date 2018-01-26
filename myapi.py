#!/usr/bin/python
import os
import sys
import commands as cmd
import pickle

def has_extension(filename,extensions):
    '''
    Check if the given filename's extension is within
    the allowed
    '''
    for allowd in extensions:
        if '.'+allowd in filename:
            return True
    return False

def get_file_list(path, extensions=None):
    '''
    Returns the list of files in a given
    filepath recursively
    '''
    files_list = []
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            if extensions:
                for ext in extensions:
                    if has_extension(filename,extensions):
                        files_list.append(os.path.join(dirpath,filename))
            else:
                files_list.append(os.path.join(dirpath,filename))
    return files_list


def sanitize(value):
    '''
    Se usa para crear strings comparables y que
    puedan ser usadas como ids. Ejemplo:
    CADENA != cadena
    '''
    value = value.strip()
    value = value.replace('\xc3\x81', 'A')
    value = value.replace('\xc3\x89', 'E')
    value = value.replace('\xc3\x8d', 'I')
    value = value.replace('\xc3\x93', 'O')
    value = value.replace('\xc3\x9a', 'U')
    value = value.replace('\xc3\x91', 'N')
    value = value.replace('\xc3\xa1', 'a')
    value = value.replace('\xc3\xa9', 'e')
    value = value.replace('\xc3\xad', 'i')
    value = value.replace('\xc3\xb3', 'o')
    value = value.replace('\xc3\xba', 'u')
    value = value.replace('\xc3\xb1', 'n')
    value = value.lower()
    value = value.replace('.', '_')
    value = value.replace(' ', '_')
    value = value.replace('\n', '')
    value = value.replace('&', 'and')
    return value


def save_data(data_file,data):
    '''
    Save data into data_file using
    pickle library
    '''
    handler = open(data_file, 'wb')
    pickle.dump(data, handler)
    handler.close()	

def load_data(data_file):
    '''
    Retrieve data from data_file
    '''
    log = open(data_file, 'rb')
    data = pickle.load(log)
    log.close()	
    return data
