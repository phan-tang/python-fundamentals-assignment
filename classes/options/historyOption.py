from .option import Option
from constants import *

class HistoryOption(Option):
    def __init__(self, car_identity_value) -> None:
        super().__init__(car_identity_value)
        self.check_folder_exist(history_folder_name)
        self.total_payment_information = self.read_file_content(f'./{main_folder_name}/{pickup_folder_name}/{self.car_identity}/{payment_file_name}.txt')
        self.available_credits_information = self.read_file_content(f'./{main_folder_name}/{pickup_folder_name}/{self.car_identity}/{credit_file_name}.txt')
        self.history_information = self.read_file_content(f'./{main_folder_name}/{pickup_folder_name}/{self.car_identity}/{history_file_name}.txt')
        self.history_file_path = f'./{main_folder_name}/{history_folder_name}/{self.car_identity}.txt'

    def export_total_payment_information(self) -> None:
        total_payment = 0
        for item in self.total_payment_information:
            total_payment += float(item)
        self.write_file(f'Total payment: ${total_payment}\n', self.history_file_path, 'w')

    def export_available_credits_information(self) -> None:
        available_credits = 0
        for item in self.available_credits_information:
            available_credits += float(item)
        self.write_file(f'Available credits: ${available_credits}\n', self.history_file_path, 'a')

    def export_history_information(self) -> None:
        self.write_file('Parked Dates:\n', self.history_file_path, 'a')
        for index, item in enumerate(self.history_information):
            self.write_file(f'{item} ${float(self.total_payment_information[index])}\n', self.history_file_path, 'a')

    def execute(self) -> None:
        self.export_total_payment_information()
        self.export_available_credits_information()
        self.export_history_information()
        print('Successfully export your parking history!')