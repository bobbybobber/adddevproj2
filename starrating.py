class starrating:
    count_id = 0
    def __init__(self, email, comment, stars):
        starrating.count_id += 1
        self.__user_id = starrating.count_id
        # , email2, password2
        self.__email = email
        self.__comment = comment
        self.__stars = stars
        # self.__email2 = "awdawda"
        # self.__password2 = "awdwadaada"

    def email_get(self):
        return self.__email
    def email_set(self,email):
        self.__email = email
    def comment_get(self):
        return self.__comment
    def getthecommentpls(self):
        return self.__comment
    def stars_get(self):
        return self.__stars
    def set_comment(self, comment):
        self.__comment = comment
    def get_user_id(self):
        return self.__user_id
    def stars_get2(self):
        return self.__comment
    def stars_set(self,stars):
        self.__stars = stars