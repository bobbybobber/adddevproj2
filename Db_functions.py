import shelve
from Customers import customer
from blog import blog
from starrating import starrating
import os
from current import current
import bcrypt

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
def get_key(my_dict):
    if len(my_dict) == 0:
        my_key = 1
    else:
        my_key = len(my_dict.keys()) + 1
    return my_key


def add_customer(customer):
    customer_dict = {}
    db = shelve.open('customer.db', 'c')

    try:
        customer_dict = db['Customer']
    except:
        print("Error in retrieving Customer from customer.db.")

    # Hash the customer's password before storing
    hashed_password = hash_password(customer.get_password())
    customer.set_password(hashed_password)

    customer.set_customer_id(get_key(customer_dict))
    customer_dict[customer.get_email()] = customer
    db['Customer'] = customer_dict
    print(customer.get_first_name(), customer.get_last_name(), "was stored in customer.db successfully with user_id ==",
          customer.get_customer_id())
    db.close()


def add_staff(staff):
    staff_dict = {}
    db = shelve.open('staff.db', 'c')
    try:
        staff_dict = db['Staff']
    except:
        print("Error in retrieving Staff from Staff.db.")

    staff.set_id(get_key(staff_dict))
    staff_dict[staff.get_email()] = staff
    db['Staff'] = staff_dict
    # Test codes
    print(staff.get_id(),staff.get_name(),staff.get_phonenumber(),staff.get_email(),
          staff.get_address(),staff.get_password())
    db.close()

def add_blog(blog):
    blog_dict = {}
    db = shelve.open('blog.db', 'c')
    try:
        blog_dict = db['Blog']
    except:
        print("Error in retrieving blog from blog.db.")

    blog.set_blog_id(get_key(blog_dict))
    blog_dict[blog.get_blog_id()] = blog
    print(blog.get_blog_image,'phase1')
    db['Blog'] = blog_dict
    # Test codes
    print(blog.get_name(), "was stored in blog.db successfully with user_id ==",
          blog.get_blog_id(), 'image was file', blog.get_blog_image(),"was saved")
    db.close()

def add_comment(comment):
    comment_dict = {}
    db = shelve.open('comment.db', 'c')
    try:
        comment_dict = db['comments']
    except:
        print("Error in retrieving comments from comment.db.")

    comment.set_comment(comment)
    comment_dict[comment.get_user_id()] = comment
    db['comments'] = comment_dict
    # Test codes
    db.close()

def add_project(project):
    project_dict = {}
    db = shelve.open('project.db', 'c')
    try:
        project_dict = db['Project']
    except:
        print("Error in retrieving Users from user.db.")

    project.set_owner_id(get_key(project_dict))
    project_dict[project.get_owner_id()] = project
    db['Project'] = project_dict
    print(project.get_phone(), "was stored in blog.db successfully with user_id ==",
          project.get_owner_id())
    # Test codes
    db.close()

def add_rating(starrating):
    rating_dict = {}
    db = shelve.open('rating.db','c')
    try:
        rating_dict = db['Rating']
    except:
        print("Error in retrieving")

    starrating.set_id(get_key(rating_dict))
    rating_dict[starrating.get_id()] = starrating
    db['Rating'] = rating_dict
    db.close()

def add_current(current):
    current_dict = {}
    db = shelve.open('current.db','c')
    try:
        current_dict = db['Current']
    except:
        print("Error in retrieving")

    current_dict['currentsession'] = current
    db['Current'] = current_dict
    print(current_dict)
    print(current)
    print(current_dict['currentsession'])
    db.close()