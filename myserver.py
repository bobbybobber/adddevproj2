from flask import Flask, render_template, request, redirect, url_for, flash,jsonify
from Customers import customer
from Staff import staff
from Forms import *
from Db_functions import *
from werkzeug.utils import *
from User import User
from project import Project
from logincheck import logincheck
from flask_mail import Mail,Message
import os
import uuid
from random import *

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'supersecretkey'
UPLOAD_FOLDER = os.path.join('static', 'image')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['UPLOAD_FOLDER'] = 'C:\\Users\\Ervin\\Desktop\\adddevproj2\\static\\image'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
def save_image(file):
    filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filename)
    return filename
#
mail = Mail(app)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'ruihernh@gmail.com'
app.config['MAIL_PASSWORD'] = 'yqqh pwcr byeq sseo'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
otp = randint(000000,999999)

# @app.route('/viewprofile/<string:email>')
# def viewprofile(email):
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/verify', methods=['POST','GET'])
def verify():
    create_email_veri_form = emailfield(request.form)
    if request.method == 'POST' and create_email_veri_form.validate():
        email = request.form['email']
        msg = Message(subject='OTP', sender='ruihernh@gmail.com', recipients=[email])
        msg.body = str(otp)

        # Use the App Password instead of your account password
        app_password = "yqqh pwcr byeq sseo"
        mail.send(msg)
        return redirect(url_for('validate', email=email))

    return render_template('getOTP.html', form=create_email_veri_form)
@app.route('/validate', methods=['GET', 'POST'])
def validate():
    email = request.args.get('email')
    create_otp_form = otpfield(request.form)
    if request.method == 'POST' and create_otp_form.validate():

        user_otp = request.form['otp']
        if otp==int(user_otp):
            return redirect(url_for('resetPassword',email=email))



    return render_template('verifyOTP.html', form=create_otp_form)

@app.route('/resetPassword', methods=['GET', 'POST'])
def resetPassword():
    email = request.args.get('email')
    print(email)
    create_reset_form = resetpassword(request.form)
    if request.method == 'POST' and create_reset_form.validate():

        if create_reset_form.password1.data==create_reset_form.password2.data:
            db = shelve.open('customer.db', 'r')
            customer_dict = db['Customer']
            db.close()
            staff_dict = {}
            db = shelve.open('staff.db', 'r')
            staff_dict = db['Staff']
            db.close()
            print('pw is same')
            if email in customer_dict:
                db = shelve.open('customer.db', 'w')
                customer_dict = db['Customer']

                Customer = customer_dict.get(email)
                Customer.set_password(create_reset_form.password1.data)
                print(Customer.get_password())
                db['Customer'] = customer_dict
                db.close()
                return redirect(url_for('retrieveCustomers'))
            elif email in staff_dict:
                db = shelve.open('staff.db','w')
                staff_dict = db['Staff']

                Staff = staff_dict.get(email)
                Staff.set_password(create_reset_form.password2.data)
                print(Staff.get_password())
                db['Staff'] = staff_dict
                db.close()
                return redirect(url_for('retrieveStaff'))
            else:
                print('wawrawrawrwasd')

    return render_template('resetPassword.html', form=create_reset_form)


@app.route('/', methods=['GET', 'POST'])
def home():

    create_login_form = logininformation(request.form)
    if request.method == 'POST' and create_login_form.validate():
        customer = logincheck(create_login_form.email.data, create_login_form.password.data)
        customer_dict = {}
        db = shelve.open('customer.db', 'r')
        customer_dict = db['Customer']
        db.close()
        staff_dict = {}
        db = shelve.open('staff.db', 'r')
        staff_dict = db['Staff']
        db.close()
        if customer.email_get() in customer_dict:
            user = customer_dict.get(customer.email_get())
            if customer.password_get() == user.get_password():
                return redirect(url_for('retrieveCustomers'))
        elif customer.email_get() in staff_dict:
            print('hello')
            user = staff_dict.get(customer.email_get())
            print(user.get_password())
            if customer.password_get() == user.get_password():
                return redirect(url_for('retrieveStaff'))




    return render_template('Startpage.html',form=create_login_form)


# login
@app.route('/login', methods=['GET', 'POST'])
def login():
    create_login_form = logininformation(request.form)
    if request.method == 'POST' and create_login_form.validate():
        customer = logincheck(create_login_form.email.data, create_login_form.password.data)
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
        staff_dict = {}
        db = shelve.open('staff.db', 'c')
        try:
            staff_dict = db['Staff']
        except:
            print("Error in retrieving Staff from Staff.db.")
        db['Staff'] = staff_dict
        db.close()
        customer_dict = {}
        db = shelve.open('customer.db', 'c')
        try:
            customer_dict = db['Customer']
        except:
            print("Error in retrieving Customer from customer.db.")
        db['Customer'] = customer_dict
        db.close()
        print(staff_dict)
        print(customer_dict)
        print(Staff.get_email())
        if Staff.get_email() in customer_dict or Staff.get_email() in staff_dict:
            print("duplicate email found!")
            print("duplicate email found!")
        else:
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


@app.route("/updateStaff/<string:email>/", methods=['GET', 'POST'])
def updateStaff(email):
    Update_staff_form = CreateStaffForm(request.form)

    if request.method == 'POST' and Update_staff_form.validate():
        staff_dict = {}
        db = shelve.open('staff.db', 'w')
        staff_dict = db['Staff']

        # Check if the customer exists in the dictionary
        if email in staff_dict:
            Staff = staff_dict[email]
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
        if email in staff_dict:
            Staff = staff_dict[email]
            Update_staff_form.name.data = Staff.get_name()
            Update_staff_form.phonenumber.data = Staff.get_phonenumber()
            Update_staff_form.email.data = Staff.get_email()
            Update_staff_form.address.data = Staff.get_address()
            Update_staff_form.password.data = Staff.get_password()

            return render_template('updateStaff.html', form=Update_staff_form)

    flash('Staff not found', 'error')
    return redirect(url_for('retrieveStaff'))


@app.route("/deleteStaff/<string:email>", methods=['POST'])
def deleteStaff(email):
    staff_dict = {}

    db = shelve.open('staff.db', 'w')
    staff_dict = db['Staff']
    staff_dict.pop(email)
    db['Staff'] = staff_dict
    db.close()
    return redirect(url_for('retrieveStaff'))


# Blog CRUD
@app.route("/createblog", methods={'GET', 'POST'})
def UploadImage():
    if request.method == 'POST':
        file = request.files['image']
        name = request.form['name']
        comment = request.form['comment']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        image = os.path.join(app.config['UPLOAD_FOLDER'],filename)

        Blog = blog(name, comment, str(image))

        add_blog(Blog)
        Blog.set_blog_image(image)
        fileimage = Blog.get_blog_image()
        new_blog_card_html = render_template('blog_card.html', blog=Blog)
        print(Blog.get_name(),
                  "was stored in blog.db successfully with user_id ==",
                  Blog.get_blog_id(),'  ',Blog.get_blog_image())
        jsonify({'new_blog_card_html': new_blog_card_html})
        return redirect(url_for('retrieveblog', image=fileimage, name=name, comment=comment))
    return render_template('createBlog.html')
    # Create_blog_form = CreateBlogForm(request.form)
    # if request.method == 'POST' and Create_blog_form.validate():
    #     Blog = blog(Create_blog_form.name.data, Create_blog_form.comment.data)
    #     add_blog(Blog)
    #     print(Blog.get_name(),
    #           "was stored in blog.db successfully with user_id ==",
    #           Blog.get_blog_id())

    #     return redirect(url_for('retrieveblog'))
    # return render_template('createBlog.html', form=Create_blog_form)
    # if request.method == 'POST' and Create_blog_form.validate():
    #     file = request.files.get('file')
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
    #     Blog = blog(Create_blog_form.name.data,CreateBlogForm.comment.data,file)
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
    customer_dict = {}
    db = shelve.open('customer.db', 'r')
    customer_dict = db['Customer']
    db.close()
    Customer_list = []
    for key in customer_dict:
        customer = customer_dict.get(key)
        Customer_list.append(customer)
    blog_list = []
    for key in blog_dict:
        blog = blog_dict.get(key)
        blog_list.append(blog)
    return render_template('retrieveBlog.html', count=len(blog_list), blog_list=blog_list, Ccounter=len(Customer_list), Customer_list=Customer_list)


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
            print("update successful")
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

            return render_template('updateBlog.html', form=Update_blog_form, id=id)

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
        customer_dict = {}
        db = shelve.open('customer.db', 'c')
        try:
            customer_dict = db['Customer']
        except:
            print("Error in retrieving Customer from customer.db.")
        db['Customer'] = customer_dict
        db.close()
        staff_dict = {}
        db = shelve.open('staff.db', 'c')
        try:
            staff_dict = db['Staff']
        except:
            print("Error in retrieving Staff from Staff.db.")
        db['Staff'] = staff_dict
        db.close()
        print(Customer.get_email())
        if Customer.get_email() in staff_dict or Customer.get_email() in customer_dict:
            print("same email!")
        else:
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


@app.route('/updateCustomer/<string:email>/', methods=['GET', 'POST'])
def update_user(email):
    update_customer_form = CreateCustomerForm(request.form)

    if request.method == 'POST' and update_customer_form.validate():
        customer_dict = {}
        db = shelve.open('customer.db', 'w')
        customer_dict = db['Customer']

        # Check if the customer exists in the dictionary
        if email in customer_dict:
            Customer = customer_dict[email]
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
        if email in customer_dict:
            Customer = customer_dict[email]
            update_customer_form.first_name.data = Customer.get_first_name()
            update_customer_form.last_name.data = Customer.get_last_name()
            update_customer_form.email.data = Customer.get_email()
            update_customer_form.password.data = Customer.get_password()

            return render_template('updateCustomer.html', form=update_customer_form)

    flash('Customer not found', 'error')
    return redirect(url_for('retrieveCustomers'))


@app.route('/deleteCustomer/<string:email>', methods=['POST'])
def deleteCustomer(email):
    customer_dict = {}
    db = shelve.open('customer.db', 'w')
    customer_dict = db['Customer']
    customer_dict.pop(email)
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


@app.route('/createProject2', methods=['GET', 'POST'])
def create_Project2():
    create_project_form = CreateProject(request.form)
    if request.method == 'POST':

        project = Project(create_project_form.address.data,create_project_form.phone.data,create_project_form.house_type.data,
                          create_project_form.house_theme.data, create_project_form.comments.data)

        add_project(project)
        print(project.get_phone(),"was stored in project.db successfully with project_id ==", project.get_owner_id())
        print(project)
        return redirect(url_for('retrieveProject'))
    return render_template('createProject2.html',form = create_project_form)

@app.route('/retrieveProject')
def retrieveProject():
    project_dict = {}
    db = shelve.open('project.db', 'r')
    project_dict = db['Project']
    db.close()
    # comment_list = []
    # for key in comment_dict:
    #     comment = comment_dict.get(key)
    #
    #     comment_list.append(comment)
    project_list = []
    for key in project_dict:
        project = project_dict.get(key)
        project_list.append(project)
        print(project.get_owner_id())
        print(project)
    return render_template('retrieveProject.html',  project_list=project_list)

# @app.route('/updateProject/<int:id>/', methods=['GET', 'POST'])
# def update_project(id):
#     update_project_form = CreateProject2(request.form)
#     if request.method == 'POST' and update_project_form.validate():
#         project_dict = {}
#         db = shelve.open('project.db', 'w')
#         project_dict = db['Project']
#         project = project_dict.get(id)
#
#         project.set_address(update_project_form.address.data)
#         project.set_comments(update_project_form.comments.data)
#         db['Project'] = project_dict
#         db.close()
#         return redirect(url_for('retrieveProject'))
#     else:
#         return redirect(url_for('retrieveProject'))
@app.route('/updateProject/<int:id>/', methods=['GET', 'POST'])
def update_project(id):
    update_project_form = CreateProject2(request.form)

    if request.method == 'POST' and update_project_form.validate():
        project_dict = {}
        db = shelve.open('project.db', 'w')
        try:
            project_dict = db['Project']
        except KeyError:
            pass

        if id in project_dict:
            project = project_dict[id]
            project.set_address(update_project_form.address.data)
            project.set_comments(update_project_form.comments.data)
            db['Project'] = project_dict
            db.close()
            flash('Project updated successfully', 'success')
            return redirect(url_for('retrieveProject'))

    else:
        project_dict = {}
        db = shelve.open('project.db', 'r')
        try:
            project_dict = db['Project']
        except KeyError:
            pass
        db.close()

        if id in project_dict:
            project = project_dict[id]
            update_project_form.address.data = project.get_address()
            update_project_form.comments.data = project.get_comments()

            return render_template('updateProject.html', form=update_project_form)

    flash('Project not found', 'error')
    return redirect(url_for('retrieveProject'))

@app.route('/deleteProject/<int:id>', methods=['POST'])
def delete_project(id):
    project_dict = {}
    db = shelve.open('project.db', 'w')
    project_dict = db['Project']
    project_dict.pop(id)
    db['Project'] = project_dict
    db.close()
    return redirect(url_for('retrieveProject'))

if __name__ == '__main__':
    app.run(debug=True)
