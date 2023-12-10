import re
from abc import ABC, abstractmethod
import os
from constants import *

class Option(ABC):
    def __init__(self, car_identity_value) -> None:
        self.car_identity = car_identity_value
        self.time_format = time_format

    @property
    def car_identity(self) -> str:
        return self.__car_identity

    @car_identity.setter
    def car_identity(self, value) -> None:
        valid = False
        r = re.compile(r'([a-zA-Z0-9]{1,3})(-[a-zA-Z0-9]{5,9})$')
        while not valid:
            try:
                if r.match(value):
                    self.__car_identity = value
                    valid = True
                else:
                    raise ValueError("Car identity must be XXX-XXXXX")
            except Exception as e:
                print(f'Error message: {e}')
                value = input('Please input your car identity: ')


    @abstractmethod
    def execute(self) -> None:
        pass

    def check_folder_exist(self, path) -> None:
        if not os.path.exists(f'./{main_folder_name}/{path}'):
            os.mkdir(f'./{main_folder_name}/{path}')

    def read_file_content(self, path, mode = 'r') -> None:
        with open(path, mode) as f:
            return [line.strip() for line in f.readlines()] 

    def write_file(self, content, file_path, mode = 'w', message = None) -> None:
        f = open(file_path, mode)
        f.write(content)
        f.close()
        if message is not None:
            print(message)