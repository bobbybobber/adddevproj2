class blog:
    count_id = 0
    def __init__(self,name,comment,image):
        blog.count_id += 1
        self.__blog_id = blog.count_id
        self.__name = name
        self.__comment = comment
        self.__image = image

    def get_blog_image(self):
        return self.__image

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

    def set_blog_image(self, images):
        # Check if self.__image already exists and is a list
        if hasattr(self, '_blog__image') and isinstance(self.__image, list):
            # If 'images' is already a list, extend the existing list
            if isinstance(images, list):
                self.__image.extend(images)
            else:
                # If 'images' is a single image, append it to the existing list
                self.__image.append(images)
        else:
            # If self.__image doesn't exist or isn't a list, create a new list
            if isinstance(images, list):
                self.__image = images
            else:
                self.__image = [images]
