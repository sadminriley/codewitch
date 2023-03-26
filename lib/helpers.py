#!/usr/bin/env python3.11
import logging
import os
import uuid


Logger = logging.getLogger(__name__)

logging.basicConfig(filename='codewitch.log', encoding='utf-8', level=logging.INFO)


# Function for searching all files in any directory

def searching_all_files(directory=os.getcwd()):
    '''
    Returns a list type of all files in the directory.
    Defaults to cwd.
    '''
    dirpath = Path(directory)
    assert dirpath.exists()
    file_list = []
    for x in dirpath.iterdir():
        if x.is_file():
            file_list.append(x)
        elif x.is_dir():
            file_list.extend(searching_all_files(x))
    return file_list


UNIQUE_LOG_ID = str(uuid.uuid4().int & (1 << 64) - 1)


def log_info(func_name, tags=None) -> None:
    Logger.info(func_name, tags)


def log_error(func_name, tags=None) -> None:
    Logger.error(func_name, tags)

