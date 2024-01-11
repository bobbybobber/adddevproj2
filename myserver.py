from flask import Flask, render_template, request, redirect, url_for, flash
from Customers import customer
from Staff import staff
from Forms import *
from Db_functions import *
from werkzeug.utils import *
from User import User
from logincheck import logincheck
import os

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_fOLDER'] = 'static/files'


# app.config['UPLOAD_FOLDER'] = 'C:\\RH stuff\\appdevProject2\\static\\Upload'
# ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


@app.route('/')
def home():
    return render_template('startpage.html')

#login
@app.route('/login', methods=['GET', 'POST'])
def login():

    create_login_form = logininformation(request.form)
    if request.method == 'POST' and create_login_form.validate():
        customer = logincheck(request.form['email'],request.form['password'])
        customer_dict = {}
        db = shelve.open('customer.db', 'r')
        customer_dict = db['Customer']
        if customer.email_get() in customer_dict:
            user = customer_dict.get(customer.email_get())

            if customer.password_get() == user.get_password():
                return redirect(url_for('retrieveCustomers'))
        db.close()



    return render_template('login.html', form=create_login_form)

# Customer Name and comment CRUD
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
#
#
# def get_filenames(directory_path):
#     if os.path.exists(directory_path):
#         return os.listdir(directory_path)
#     else:
#         print(f"The directory '{directory_path}' does not exist.")
#         return []
# Staff CRUD
@app.route("/createStaff", methods={'GET', 'POST'})
def create_staff():
    create_Staff_form = CreateStaffForm(request.form)
    if request.method == 'POST' and create_Staff_form.validate():
        Staff = staff(create_Staff_form.name.data, create_Staff_form.phonenumber.data, create_Staff_form.email.data,
                      create_Staff_form.address.data, create_Staff_form.password.data)
        add_staff(Staff)
        print(Staff.get_name(),
              "was stored in staff.db successfully with user_id ==",
              Staff.get_id())

        return redirect(url_for('retrieveStaff'))
    return render_template('createStaff.html', form=create_Staff_form)


@app.route("/retrieveStaff")
def retrieveStaff():
    staff_dict = {}
    db = shelve.open('staff.db', 'r')
    staff_dict = db['Staff']
    db.close()

    staff_list = []
    for key in staff_dict:
        staff = staff_dict.get(key)
        staff_list.append(staff)

    return render_template('retrieveStaff.html', count=len(staff_list), staff_list=staff_list)


@app.route("/updateStaff/<int:id>/", methods=['GET', 'POST'])
def updateStaff(id):
    Update_staff_form = CreateStaffForm(request.form)

    if request.method == 'POST' and Update_staff_form.validate():
        staff_dict = {}
        db = shelve.open('staff.db', 'w')
        staff_dict = db['Staff']

        # Check if the customer exists in the dictionary
        if id in staff_dict:
            Staff = staff_dict[id]
            Staff.set_name(Update_staff_form.name.data)
            Staff.set_phonenumber(Update_staff_form.phonenumber.data)
            Staff.set_email(Update_staff_form.email.data)
            Staff.set_address(Update_staff_form.address.data)
            Staff.set_password(Update_staff_form.password.data)
            db['Staff'] = staff_dict
            db.close()
            flash('Staff updated successfully', 'success')
            return redirect(url_for('retrieveStaff'))

    else:
        staff_dict = {}
        db = shelve.open('staff.db', 'r')
        staff_dict = db['Staff']
        db.close()

        # Check if the customer exists in the dictionary
        if id in staff_dict:
            Staff = staff_dict[id]
            Update_staff_form.name.data = Staff.get_name()
            Update_staff_form.phonenumber.data = Staff.get_phonenumber()
            Update_staff_form.email.data = Staff.get_email()
            Update_staff_form.address.data = Staff.get_address()
            Update_staff_form.password.data = Staff.get_password()

            return render_template('updateStaff.html', form=Update_staff_form)

    flash('Staff not found', 'error')
    return redirect(url_for('retrieveStaff'))


@app.route("/deleteStaff/<int:id>", methods=['POST'])
def deleteStaff(id):
    staff_dict = {}
    db = shelve.open('staff.db', 'w')
    staff_dict = db['Staff']
    staff_dict.pop(id)
    db['Staff'] = staff_dict
    db.close()
    return redirect(url_for('retrieveStaff'))


# Blog CRUD
@app.route("/createblog", methods={'GET', 'POST'})
def UploadImage():
    Create_blog_form = CreateBlogForm(request.form)
    if request.method == 'POST' and Create_blog_form.validate():
        Blog = blog(Create_blog_form.name.data, Create_blog_form.comment.data)
        add_blog(Blog)
        print(Blog.get_name(),
              "was stored in blog.db successfully with user_id ==",
              Blog.get_blog_id())

        return redirect(url_for('retrieveblog'))
    return render_template('createBlog.html', form=Create_blog_form)

    # file = request.files.get('file')
    # if not file:
    #     flash('No file part')
    #     return redirect(url_for('home'))
    #
    # if file.filename == '':
    #     flash('No image selected for uploading')
    #     return redirect(request.url)
    #
    # if file and allowed_file(file.filename):
    #     filename = secure_filename(file.filename)
    #     file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    #     Blog = blog(Create_blog_form.name.data,CreateBlogForm.comment.data)
    #     add_blog(Blog)
    #     print(Blog.get_name(),
    #           "was stored in blog.db successfully with user_id ==",
    #           Blog.get_blog_id())
    #
    #     flash('Image Successfully uploaded and displayed below')
    #     return render_template('retrieveBlog.html', form=Create_blog_form)
    # else:
    #     flash('Allowed image types are - png, jpg, jpeg, gif')
    #     return redirect(url_for('retrieveblog'))

    # return render_template('createBlog.html', form=blog)


@app.route("/retrieveblog")
def retrieveblog():
    blog_dict = {}
    db = shelve.open('blog.db', 'r')
    blog_dict = db['Blog']
    db.close()

    blog_list = []
    for key in blog_dict:
        blog = blog_dict.get(key)
        blog_list.append(blog)

    return render_template('retrieveBlog.html', count=len(blog_list), blog_list=blog_list)


@app.route('/updateblog/<int:id>/', methods=['GET', 'POST'])
def update_blog(id):
    Update_blog_form = CreateBlogForm(request.form)

    if request.method == 'POST' and Update_blog_form.validate():
        blog_dict = {}
        db = shelve.open('blog.db', 'w')
        blog_dict = db['Blog']

        # Check if the customer exists in the dictionary
        if id in blog_dict:
            Blog = blog_dict[id]
            Blog.set_name(Update_blog_form.name.data)
            Blog.set_comment(Update_blog_form.comment.data)
            db['Blog'] = blog_dict
            db.close()
            flash('Blog updated successfully', 'success')
            return redirect(url_for('retrieveblog'))

    else:
        blog_dict = {}
        db = shelve.open('blog.db', 'r')
        blog_dict = db['Blog']
        db.close()

        # Check if the customer exists in the dictionary
        if id in blog_dict:
            Blog = blog_dict[id]
            Update_blog_form.name.data = Blog.get_name()
            Update_blog_form.comment.data = Blog.get_comment()

            return render_template('updateBlog.html', form=Update_blog_form)

    flash('Blog not found', 'error')
    return redirect(url_for('retrieveblog'))


@app.route('/deleteblog/<int:id>', methods=['POST'])
def deleteblog(id):
    blog_dict = {}
    db = shelve.open('blog.db', 'w')
    blog_dict = db['Blog']
    blog_dict.pop(id)
    db['Blog'] = blog_dict
    db.close()
    return redirect(url_for('retrieveblog'))


# Customer CRUD
@app.route('/createCustomer', methods=['GET', 'POST'])
def create_customer():
    create_Customer_form = CreateCustomerForm(request.form)
    if request.method == 'POST' and create_Customer_form.validate():
        Customer = customer(create_Customer_form.first_name.data, create_Customer_form.last_name.data,
                            create_Customer_form.email.data, create_Customer_form.password.data)
        add_customer(Customer)
        print(Customer.get_first_name(), Customer.get_last_name(),
              "was stored in customer.db successfully with user_id ==",
              Customer.get_customer_id())

        return redirect(url_for('retrieveCustomers'))
    return render_template('createCustomer.html', form=create_Customer_form)


@app.route('/retrieveCustomers')
def retrieveCustomers():
    customer_dict = {}
    db = shelve.open('customer.db', 'r')
    customer_dict = db['Customer']
    db.close()

    Customer_list = []
    for key in customer_dict:
        customer = customer_dict.get(key)
        Customer_list.append(customer)

    return render_template('retrieveCustomer.html', count=len(Customer_list), Customer_list=Customer_list)


@app.route('/updateCustomer/<int:id>/', methods=['GET', 'POST'])
def update_user(id):
    update_customer_form = CreateCustomerForm(request.form)

    if request.method == 'POST' and update_customer_form.validate():
        customer_dict = {}
        db = shelve.open('customer.db', 'w')
        customer_dict = db['Customer']

        # Check if the customer exists in the dictionary
        if id in customer_dict:
            Customer = customer_dict[id]
            Customer.set_first_name(update_customer_form.first_name.data)
            Customer.set_last_name(update_customer_form.last_name.data)
            Customer.set_email(update_customer_form.email.data)
            db['Customer'] = customer_dict
            db.close()
            flash('Customer updated successfully', 'success')
            return redirect(url_for('retrieveCustomers'))

    else:
        customer_dict = {}
        db = shelve.open('customer.db', 'r')
        customer_dict = db['Customer']
        db.close()

        # Check if the customer exists in the dictionary
        if id in customer_dict:
            Customer = customer_dict[id]
            update_customer_form.first_name.data = Customer.get_first_name()
            update_customer_form.last_name.data = Customer.get_last_name()
            update_customer_form.email.data = Customer.get_email()
            update_customer_form.password.data = Customer.get_password()

            return render_template('updateCustomer.html', form=update_customer_form)

    flash('Customer not found', 'error')
    return redirect(url_for('retrieveCustomers'))


@app.route('/deleteCustomer/<int:id>', methods=['POST'])
def deleteCustomer(id):
    customer_dict = {}
    db = shelve.open('customer.db', 'w')
    customer_dict = db['Customer']
    customer_dict.pop(id)
    db['Customer'] = customer_dict
    db.close()
    return redirect(url_for('retrieveCustomers'))

@app.route('/updatecomment/<int:id>/', methods=['GET', 'POST'])
def update_comment(id):
    update_comment_form = ratingcomment2(request.form)
    if request.method == 'POST' and update_comment_form.validate():
        comment_dict = {}
        db = shelve.open('comment.db', 'w')
        comment_dict = db['comments']
        comment = comment_dict.get(id)
        print(comment_dict.get(id))
        comment.set_comment(update_comment_form.comment.data)
        comment.stars_set(update_comment_form.stars.data)
        db['comments'] = comment_dict
        db.close()
        print('works?')
        return redirect(url_for('rating'))

    else:
        return render_template('updatecomment.html', form=update_comment_form)

@app.route('/viewproject')
def view_project():
    return render_template('viewproject.html')

@app.route('/rating', methods=['GET', 'POST'])
def rating():
    # users_list = []
    # for key in users_dict:
    #     user = users_dict.get(key)
    #     users_list.append(user)
    comment_dict = {}
    db = shelve.open('comment.db', 'r')
    comment_dict = db['comments']
    print(comment_dict)
    db.close()
    comment_list = []
    for key in comment_dict:
        comment = comment_dict.get(key)

        comment_list.append(comment)
    create_rating_form = ratingcomment(request.form)
    if request.method == 'POST' and create_rating_form.validate():
        users_dict = {}
        db = shelve.open('user.db', 'r')
        users_dict = db['Users']

        comment1 = starrating(create_rating_form.email.data, create_rating_form.comment.data,
                              create_rating_form.stars.data)
        if comment1.email_get() in users_dict:
            db.close()
            print(comment1)
            add_comment(comment1)

            return redirect(url_for('rating'))

    return render_template('rating.html', form=create_rating_form, count=len(comment_list), users_list=comment_list)


@app.route('/deleteComment/<int:id>', methods=['POST'])
def deleteComment(id):
    print(id)
    comment_dict = {}
    db = shelve.open('comment.db', 'w')
    comment_dict = db['comments']
    comment_dict.pop(id)
    db['comments'] = comment_dict
    db.close()
    return redirect(url_for('rating'))


if __name__ == '__main__':
    app.run(debug=True)
