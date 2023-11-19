import re
from abc import ABC, abstractmethod

class Option(ABC):
    def __init__(self, car_identity_value) -> None:
        self.car_identity = car_identity_value
        self.time_format = "%Y-%m-%d %H:%M"

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