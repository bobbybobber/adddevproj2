from User import User
class Project:
    count_id = 0
    def _init_(self, address, phone,  house_type, house_theme, comments):
        User.count_id += 1
        self.__user_id = Project.count_id
        self.__house_type = house_type
        self.__house_theme = house_theme
        self.__address = address
        self.__phone = phone
        self.__comments = comments

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