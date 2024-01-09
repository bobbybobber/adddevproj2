class blog:
    count_id = 0
    def __init__(self,name,comment):
        blog.count_id += 1
        self.__blog_id = blog.count_id
        self.__name = name
        self.__comment = comment

    def get_blog_id(self):
        return self.__blog_id
    def get_name(self):
        return self.__name

    def get_comment(self):
        return self.__comment

    def set_blog_id(self,id):
        self.__blog_id = id

    def set_name(self, name):
        if name is not None:
            self.__name = name
        else:
            print("Invalid name provided.")

    def set_comment(self, comment):
        self.__comment = comment