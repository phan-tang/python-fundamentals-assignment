from .options import *

class ParkingSystem:
    def __init__(self) -> None:
        self.__options = ['Park', 'Pickup', 'History', 'Cancel']
        self.option = None

    def get_option_class(self, option_chosen, car_identity) -> None:
        if option_chosen == 1:
            self.option = ParkOption(car_identity)
        if option_chosen == 2:
            self.option = PickupOption(car_identity)
        if option_chosen == 3:
            self.option = HistoryOption(car_identity)

    def run(self) -> None:
        running = True
        while running:
            try:
                print('-----Welcome to Parking System-----')
                for index, option in enumerate(self.__options):
                    print(f"{index + 1} - {option}\t")
                option_chosen = input('Please choose one of three options by entering the number: ')
                if int(option_chosen) <= len(self.__options) and self.__options[int(option_chosen)-1] != 'Cancel':
                    car_identity = input('Please input your car identity: ')
                    self.get_option_class(int(option_chosen), car_identity)
                    self.option.execute()
                else:
                    running = False
                    print('Exited')
            except Exception as e:
                print("Error message:", e)
            