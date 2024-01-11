from Customers import customer
class logincheck:
    def __init__(self, email2, password2):
        customer.count_id += 1
        # , email2, password2
        self.__email2 = email2
        self.__password2 = password2
        # self.__email2 = "awdawda"
        # self.__password2 = "awdwadaada"

    def logincheckfunc(self):
        print("it means its works!!!!! you hear that yishun~~!!!!!!!! bob")

    def logincheckfunc2(self):
        print("it means its works!!!!! you hear that yishun~~!!!!!!!! bob22222222")
    def email_get(self):
        return self.__email2

    def password_get(self):
        return self.__password2

    def email_set(self,email):
        self.__email2 = email
    def password_set(self,password):
        self.__password2 = password