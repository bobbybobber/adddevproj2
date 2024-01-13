import shelve
class customer:
    count_id = 0

    # initializer method
    def __init__(self, first_name, last_name,email,password):
        customer.count_id += 1
        self.__customer_id = customer.count_id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__email = email
        self.__password = password


    # accessor methods
    def get_customer_id(self):
        return self.__customer_id

    def get_first_name(self):
        return self.__first_name

    def get_last_name(self):
        return self.__last_name

    def get_email(self):
        return  self.__email
    def get_password(self):
        return  self.__password
    # mutator methods
    def set_customer_id(self, user_id):
        self.__customer_id = user_id

    def set_first_name(self, first_name):
        self.__first_name = first_name

    def set_last_name(self, last_name):
        self.__last_name = last_name

    def set_email(self,email):
        self.__email = email
    def set_password(self,password):
        self.__password = password