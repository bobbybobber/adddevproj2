from User import User
from datetime import datetime
class Project:
    count_id = 0
    def __init__(self, address, phone,  house_type, house_theme, comments,start_date=None):
        Project.count_id += 1
        self.__user_id = Project.count_id
        self.__house_type = house_type
        self.__house_theme = house_theme
        self.__address = address
        self.__phone = phone
        self.__comments = comments
        self.__start_date = start_date if start_date else datetime.now()

    def get_owner_id(self):
        return self.__user_id
    def get_phone(self):
        return self.__phone

    def get_address(self):
        return self.__address

    def get_house_type(self):
        return self.__house_type

    def get_house_theme(self):
        return self.__house_theme

    def get_comments(self):
        return self.__comments

    def set_owner_id(self,owner_id):
        self.__owner_id = owner_id
    def set_phone(self,phone):
        self.__phone = phone

    def set_address(self, address):
        self.__address = address

    def set_house_type(self,house_type):
        self.__house_type = house_type

    def set_house_theme(self,house_theme):
        self.__house_theme = house_theme

    def set_comments(self,comments):
        self.__comments = comments

    def get_start_date(self):
        return self.__start_date
    def set_start_date(self,start_date):
        self.__start_date = start_date
    def set_remaining_time(self, remaining_time):
        self.__remaining_time = remaining_time

    def get_remaining_time(self):
        return self.__remaining_time

    def calculate_progress(self):
        # Assuming you have a total duration in days (you can adjust as needed)
        total_duration_days = self.get_duration() * 30
        progress_percentage = ((total_duration_days - self.get_remaining_time()) / total_duration_days) * 100
        return max(min(progress_percentage, 100), 0)  # Clamp value between 0 and 100

    def get_duration(self):
        combination_durations = {
            "1-Room HDB, Scandinavian": 1,
            "1-Room HDB, Luxury": 2,
            "1-Room HDB, Modern-Luxury": 3,
            "1-Room HDB, Traditional": 4,
            "1-Room HDB, Contemporary": 5,
            "1-Room HDB, Farmhouse": 6,
            "2-Room HDB, Scandinavian": 7,
            "2-Room HDB, Luxury": 8,
            "2-Room HDB, Modern-Luxury": 9,
            "2-Room HDB, Traditional": 10,
            "2-Room HDB, Contemporary": 11,
            "2-Room HDB, Farmhouse": 12,
            "3-Room HDB, Scandinavian": 13,
            "3-Room HDB, Luxury": 14,
            "3-Room HDB, Modern-Luxury": 15,
            "3-Room HDB, Traditional": 16,
            "3-Room HDB, Contemporary": 17,
            "3-Room HDB, Farmhouse": 18,
            "4-Room HDB, Scandinavian": 19,
            "4-Room HDB, Luxury": 20,
            "4-Room HDB, Modern-Luxury": 21,
            "4-Room HDB, Traditional": 22,
            "4-Room HDB, Contemporary": 23,
            "4-Room HDB, Farmhouse": 24,
            "5-Room HDB, Scandinavian": 25,
            "5-Room HDB, Luxury": 26,
            "5-Room HDB, Modern-Luxury": 27,
            "5-Room HDB, Traditional": 28,
            "5-Room HDB, Contemporary": 29,
            "5-Room HDB, Farmhouse": 30
        }
        # Calculate the duration based on house type and theme
        combination_key = f"{self.__house_type}, {self.__house_theme}"
        duration_months = combination_durations.get(combination_key, 0)
        return duration_months * 30  # Assuming the duration is in days