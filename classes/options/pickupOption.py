from .option import Option
from datetime import datetime, timedelta
import numpy as np
import os
from constants import *

class PickupOption(Option):
    def __init__(self, car_identity_value) -> None:
        super().__init__(car_identity_value)
        self.pickup_time = input('Please enter the pickup time: ')
        self.time_list = time_list
        self.price_list = price_list
        self.discount_list = discount_list
        self.parking_information = self.get_parking_information()
        self.check_folder_exist(pickup_folder_name)
        self.check_folder_exist(f'{pickup_folder_name}/{self.car_identity}')
        self.parking_price = self.calculate_parking_price()
    
    @property
    def pickup_time(self) -> str:
        return self.__pickup_time
    
    @pickup_time.setter
    def pickup_time(self, value) -> None:
        valid = False
        while not valid:
            try:
                value = value + ':00' if value.count(':') < 2 else value
                self.__pickup_time = datetime.strptime(value, self.time_format)
                valid = True
            except Exception as e:
                print(f'Error message: {e}')
                value = input('Please enter the arrival time: ')

    def get_parking_information(self) -> None:
        try:
            file_path = f"./{main_folder_name}/{park_folder_name}/{self.car_identity}.txt"
            content = self.read_file_content(file_path)[0]
            return [item.strip() for item in content.split(',')]
        except Exception as e:
            raise FileNotFoundError(f'No valid identity found')

    def transform_time_to_integer(self, time) -> float:
        return time.hour + time.minute/60

    def get_parking_time_of_days(self, parked_datetime) -> list:
        start_week_day = parked_datetime.weekday()
        if self.pickup_time.date() == parked_datetime.date():
            parking_time_of_days = [[start_week_day, parked_datetime, self.pickup_time, self.pickup_time - parked_datetime]]
        else:
            second_date = datetime(parked_datetime.year, parked_datetime.month, parked_datetime.day) + timedelta(days=1)
            hours_in_first_day = (second_date - parked_datetime).seconds/3600 if [parked_datetime.hour, parked_datetime.minute, parked_datetime.second] != [0, 0, 0] else 24
            parking_time_of_days = [[start_week_day, parked_datetime, second_date, hours_in_first_day]]
            last_date = datetime(self.pickup_time.year, self.pickup_time.month, self.pickup_time.day)
            parking_time_of_days.extend([[((start_week_day + day + 1) % 7), second_date + timedelta(days=day), second_date + timedelta(days=day+1), 24] for day in range((last_date - second_date).days)])
            parking_time_of_days.append([self.pickup_time.weekday(), last_date, self.pickup_time, (self.pickup_time - last_date).seconds/3600])
        return parking_time_of_days

    def get_parking_time_in_each_time_ranges(self, parking_time_of_day) -> list:
        if parking_time_of_day[:-1] == 24:
            return [8, 8, 8]
        parked_time_in_each_time_ranges = []
        start_time = self.transform_time_to_integer(parking_time_of_day[1])
        end_time = self.transform_time_to_integer(parking_time_of_day[2]) if parking_time_of_day[2].hour != 0 and parking_time_of_day[2].minute != 0 else 24
        for time_range in self.time_list:
            if start_time >= time_range[1]:
                parked_time_in_each_time_ranges.append(0)
            else:
                start_time_in_range = start_time if start_time > time_range[0] else time_range[0]
                end_time_in_range = end_time if time_range[1] > end_time else time_range[1]
                parked_time_in_each_time_ranges.append(end_time_in_range - start_time_in_range)
        return parked_time_in_each_time_ranges

    def get_parking_price_in_each_time_range(self, parked_time_in_each_time_range, price_list_item, index) -> float:
        hours = np.ceil(parked_time_in_each_time_range)
        return price_list_item[index][0] * price_list_item[index][1] + (2 * price_list_item[index][1] * (hours - price_list_item[index][0])) if hours > price_list_item[index][0] else hours * price_list_item[index][1]

    def get_parking_price_in_each_day(self, parking_time_of_day) -> float:
        price_of_parking_time_each_day = 0
        price_list_item = self.price_list[list(self.price_list.keys())[parking_time_of_day[0]]]
        parked_time_in_each_time_ranges = self.get_parking_time_in_each_time_ranges(parking_time_of_day)
        for index, parked_time_in_each_time_range in enumerate(parked_time_in_each_time_ranges):
            if parked_time_in_each_time_range > 0:
                price = price_list_item[index][1] if index == 0 else self.get_parking_price_in_each_time_range(parked_time_in_each_time_range, price_list_item, index)
                price_of_parking_time_each_day += price * (1 - self.get_discount_percent(index))
        return price_of_parking_time_each_day

    def get_discount_percent(self, index) -> float:
        if self.parking_information[-1] == 'None':
            return 0
        return self.discount_list[index]

    def calculate_parking_price(self) -> float:
        parking_price = 0
        parked_datetime = datetime.strptime(self.parking_information[1], self.time_format)
        parking_time_of_days = self.get_parking_time_of_days(parked_datetime)
        for parking_time_of_day in parking_time_of_days:
            parking_price += self.get_parking_price_in_each_day(parking_time_of_day)
        return parking_price

    def pay_parking_price(self) -> None:
        valid = False
        while not valid:
            payment_amount = input('Please input your payment amount (must be equal to or greater than total parking price): ')
            if float(payment_amount) >= self.parking_price:
                valid = True
                self.write_total_payment()
                self.write_available_credits(round(float(payment_amount) - self.parking_price, 2))
                self.write_parking_history()

    def write_total_payment(self):
        total_payment_file_path = f"./{main_folder_name}/{pickup_folder_name}/{self.car_identity}/{payment_file_name}.txt"
        self.write_file(f'{self.parking_price}\n', total_payment_file_path, 'a')

    def write_available_credits(self, available_credits):
        available_credits_file_path = f"./{main_folder_name}/{pickup_folder_name}/{self.car_identity}/{credit_file_name}.txt"
        self.write_file(f'{available_credits}\n', available_credits_file_path, 'a')

    def write_parking_history(self) -> None:
        history_file_path = f"./{main_folder_name}/{pickup_folder_name}/{self.car_identity}/{history_file_name}.txt"
        content = f'{self.parking_information[1]} - {self.pickup_time}\n'
        self.write_file(content, history_file_path, 'a')
        os.remove(f"./{main_folder_name}/{park_folder_name}/{self.car_identity}.txt")

    def execute(self) -> None:
        print(f'Total parking price: {self.parking_price}')
        self.pay_parking_price()
        print('Successfully pay your parking price!')