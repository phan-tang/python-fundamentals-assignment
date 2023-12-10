from .option import Option
from datetime import datetime
from constants.folderNames import *

class ParkOption(Option):
    def __init__(self, car_identity_value) -> None:
        super().__init__(car_identity_value)
        self.arrival_time = input('Please enter the arrival time: ')
        self.frequent_parking_number = input('Please enter the frequent parking number: ')
        self.check_folder_or_file_exist(park_folder_name)

    @property
    def arrival_time(self) -> str:
        return self.__arrival_time
    
    @arrival_time.setter
    def arrival_time(self, value) -> None:
        valid = False
        while not valid:
            try:
                value = value + ':00' if value.count(':') < 2 else value
                self.__arrival_time = datetime.strptime(value, self.time_format)
                valid = True
            except Exception as e:
                print(f'Error message: {e}')
                value = input('Please enter the arrival time: ')

    @property
    def frequent_parking_number(self) -> str:
        return self.__frequent_parking_number
    
    @frequent_parking_number.setter
    def frequent_parking_number(self, value) -> None:
        self.__frequent_parking_number = self.check_frequent_parking_number_by_modulo_11(value)

    def check_frequent_parking_number_by_modulo_11(self, value) -> None | str:
        sum_digits = 0
        for digit_index, digit in enumerate(value):
            sum_digits += (int(digit) * (len(value) - digit_index))
            print(f'{digit} * {(len(value) - digit_index)}')
        return value if sum_digits % 11 == 0 else None

    def execute(self) -> None:
        content = f'{self.car_identity} , {self.arrival_time} , {self.frequent_parking_number}'
        message = f'Finished writing parking file for {self.car_identity}'
        self.write_file(content, message, park_folder_name)