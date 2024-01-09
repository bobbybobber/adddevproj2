import shelve
from Customers import customer
from blog import blog
def get_key(my_dict):
    if len(my_dict)==0:
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

    customer.set_customer_id(get_key(customer_dict))
    customer_dict[customer.get_email()] = customer
    db['Customer'] = customer_dict
    # Test codes
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
    staff_dict[staff.get_id()] = staff
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
    db['Blog'] = blog_dict
    # Test codes
    print(blog.get_name(), "was stored in blog.db successfully with user_id ==",
          blog.get_blog_id())
    db.close()