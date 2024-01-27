class staff:
    count_id = 0
    def __init__(self,name,phonenumber,email,address,password,role,timein,timeout,image=None):
        staff.count_id += 1
        self.__staff_id = staff.count_id
        self.__name = name
        self.__phonenumber = phonenumber
        self.__email = email
        self.__address = address
        self.__password = password
        self.__image = '/static/image/default.jpg'
        self.__role = role
        self.__timein = timein
        self.__timeout = timeout


    def get_id(self):
        return self.__staff_id

    def get_name(self):
        return self.__name

    def get_phonenumber(self):
        return self.__phonenumber

    def get_email(self):
        return self.__email

    def get_address(self):
        return self.__address

    def get_password(self):
        return self.__password

    def set_name(self,name):
        self.__name = name

    def set_phonenumber(self,phonenumber):
        self.__phonenumber = phonenumber

    def set_email(self,email):
        self.__email = email

    def set_address(self,address):
        self.__address = address

    def set_password(self,password):
        self.__password = password

    def set_id(self,id):
        self.__staff_id = id

    def set_image(self, image):
        self.__image = image
    def get_image(self):
        return self.__image

    def get_role(self):
        return self.__role
    def set_role(self,role):
        self.__role = role

    def get_timein(self):
        return self.__timein
    def set_timein(self,timein):
        self.__timein = timein
    def get_timeout(self):
        return self.__timeout
    def set_timeout(self,timeout):
        self.__timeout = timeout