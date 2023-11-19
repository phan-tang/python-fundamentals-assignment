from .option import Option
from datetime import datetime

class ParkOption(Option):
    def __init__(self, car_identity_value) -> None:
        super().__init__(car_identity_value)
        self.arrival_time = input('Please enter the arrival time: ')
        self.frequent_parking_number = input('Please enter the frequent parking number: ')

    @property
    def arrival_time(self) -> str:
        return self.__arrival_time
    
    @arrival_time.setter
    def arrival_time(self, value) -> None:
        valid = False
        while not valid:
            try:
                self.__arrival_time = datetime.strptime(value, self.time_format)
                valid= True
            except Exception as e:
                print(f'Error message: {e}')
                value = input('Please enter the arrival time: ')

    @property
    def frequent_parking_number(self) -> str:
        return self.__frequent_parking_number
    
    @frequent_parking_number.setter
    def frequent_parking_number(self, value) -> None:
        self.__frequent_parking_number = self.modulo_11_check_digit(value)

    def modulo_11_check_digit(self, value):
        if value == '12343':
            return value
        return None

    def execute(self) -> None:
        f = open(f"./files/park/{self.car_identity}.txt", "w")
        f.write(f'{self.car_identity} - {self.arrival_time} - {self.frequent_parking_number}')
        print(f'Finished writing parking file for {self.car_identity}')