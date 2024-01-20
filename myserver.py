from datetime import timedelta

from flask import Flask, render_template, request, redirect, url_for, flash,jsonify,session
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
import bcrypt

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'supersecretkey'
UPLOAD_FOLDER = os.path.normpath(os.path.join('static', 'image'))
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['UPLOAD_FOLDER'] = 'C:\\Users\\Ervin\\Desktop\\adddevproj2\\static\\image'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

@app.context_processor
def inject_user_status():
    return dict(is_logged_in='email' in session)

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

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

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
                password = hash_password(create_reset_form.password1.data)
                Customer.set_password(password)
                print(Customer.get_password())
                db['Customer'] = customer_dict
                db.close()
                return redirect(url_for('retrieveCustomers', email=email))
            elif email in staff_dict:
                db = shelve.open('staff.db','w')
                staff_dict = db['Staff']

                Staff = staff_dict.get(email)
                password = hash_password(create_reset_form.password2.data)
                Staff.set_password(password)
                print(Staff.get_password())
                db['Staff'] = staff_dict
                db.close()
                return redirect(url_for('retrieveStaff', email=email))
            else:
                print('wawrawrawrwasd')

    return render_template('resetPassword.html', form=create_reset_form, email=email)


@app.route('/', methods=['GET', 'POST'])
def home():
    create_login_form = logininformation(request.form)
    if request.method == 'POST' and create_login_form.validate():
        email = create_login_form.email.data
        entered_password = create_login_form.password.data
        customer_dict = {}
        staff_dict = {}

        with shelve.open('customer.db', 'r') as db:
            customer_dict = db.get('Customer', {})

        with shelve.open('staff.db', 'r') as db:
            staff_dict = db.get('Staff', {})

        user = customer_dict.get(email) or staff_dict.get(email)
        if user:
            if bcrypt.checkpw(entered_password.encode('utf-8'), user.get_password()):
                session['email'] = user.get_email()
                session['user_id'] = str(uuid.uuid4())
                session['user_type'] = 'customer' if email in customer_dict else 'staff'
                return redirect(url_for('retrieveCustomers', email=email)) if session['user_type'] == 'customer' else redirect(url_for('retrieveStaff', email=email))
            else:
                flash("Invalid username or password", "danger")
        else:
            flash("Invalid username or password", "danger")
    is_logged_in = 'email' in session  # Check if user is logged in
    return render_template('Startpage.html', form=create_login_form, is_logged_in=is_logged_in)


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
    email = request.args.get('email')
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
        new_blog_card_html = render_template('blog_card.html', blog=Blog,email=email, name=name, comment=comment)
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
    email = request.args.get('email')
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
    print(Customer_list)
    return render_template('retrieveBlog.html', count=len(blog_list), blog_list=blog_list, Ccounter=len(Customer_list), Customer_list=Customer_list, email=email)


@app.route('/updateblog/<int:id>/', methods=['GET', 'POST'])
def update_blog(id):
    email = request.args.get('email')
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

            return render_template('updateBlog.html', form=Update_blog_form, id=id,email = email)

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
    email = request.args.get('email')
    customer_dict = {}
    db = shelve.open('customer.db', 'r')
    customer_dict = db['Customer']
    db.close()

    Customer_list = []
    for key in customer_dict:
        customer = customer_dict.get(key)
        Customer_list.append(customer)

    return render_template('retrieveCustomer.html', count=len(Customer_list), Customer_list=Customer_list,email=email)


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
    email = request.args.get('email')
    create_project_form = CreateProject(request.form)
    if request.method == 'POST':

        project = Project(create_project_form.address.data,create_project_form.phone.data,create_project_form.house_type.data,
                          create_project_form.house_theme.data, create_project_form.comments.data)

        add_project(project)
        print(project.get_owner_id())
        project.set_start_date(datetime.now())
        print(project.get_start_date())
        print(project.get_phone(),"was stored in project.db successfully with project_id ==", project.get_owner_id())
        print(project)
        id1 = project.get_owner_id()
        return redirect(url_for('projectSummary',id = id1, project = project , email = email))

    return render_template('createProject2.html',form = create_project_form, email=email)

@app.route('/projectSummary/<int:id>/', methods=['GET', 'POST'])
def projectSummary(id):
    email = request.args.get('email')
    project_dict = {}
    db = shelve.open('project.db', 'r')
    project_dict = db['Project']
    project = project_dict.get(id)
    db.close()


    combination_durations = {
        "1-Room HDB, Scandinavian": 1,
        "1-Room HDB, Luxury": 2,
        "1-Room HDB, Modern-Luxury": 3,
        "1-Room HDB, Traditional": 4,
        "1-Room HDB, Contemporary": 5,
        "1-Room HDB, Farmhouse": 6,
        "2-Room HDB, Scandinavian": 7,
        "2-Room HDB, Luxury": 8,
        "2-Room HDB, Modern-Luxury": 9,
        "2-Room HDB, Traditional": 10,
        "2-Room HDB, Contemporary": 11,
        "2-Room HDB, Farmhouse": 12,
        "3-Room HDB, Scandinavian": 13,
        "3-Room HDB, Luxury": 14,
        "3-Room HDB, Modern-Luxury": 15,
        "3-Room HDB, Traditional": 16,
        "3-Room HDB, Contemporary": 17,
        "3-Room HDB, Farmhouse": 18,
        "4-Room HDB, Scandinavian": 19,
        "4-Room HDB, Luxury": 20,
        "4-Room HDB, Modern-Luxury": 21,
        "4-Room HDB, Traditional": 22,
        "4-Room HDB, Contemporary": 23,
        "4-Room HDB, Farmhouse": 24,
        "5-Room HDB, Scandinavian": 25,
        "5-Room HDB, Luxury": 26,
        "5-Room HDB, Modern-Luxury": 27,
        "5-Room HDB, Traditional": 28,
        "5-Room HDB, Contemporary": 29,
        "5-Room HDB, Farmhouse": 30
    }
    project_dict = {}
    db = shelve.open('project.db', 'r')
    project_dict = db['Project']

    project = project_dict.get(id)
    project.set_email(email)
    project_dict[project.get_owner_id()] = project
    db.close()
    house_type = project.get_house_type()
    house_theme = project.get_house_theme()
    key1 = f"{house_type}, {house_theme}"
    duration_months = combination_durations.get(key1, 0)
    # Calculate total price
    base_price_per_month = 1000
    total_price = duration_months * base_price_per_month
    project.set_total_price(total_price)

    if request.method == 'POST':
        return redirect(url_for('checkout', id=id , email = email))

    return render_template('projectSummary.html', project=project, id=id,email=email)
@app.route('/checkout/<int:id>/', methods=['GET', 'POST'])
def checkout(id):
    def expiry_date_valid(expiry_date):
        # Expected format: MM/YY
        try:
            exp_date = datetime.strptime(expiry_date, "%m/%y")
            return exp_date > datetime.now()
        except ValueError:
            # If the date is not in the correct format, it's invalid
            return False
    email = request.args.get('email')
    project_dict = {}
    db = shelve.open('project.db', 'r')
    project_dict = db['Project']
    db.close()
    project = project_dict.get(id)
    if request.method == 'POST':
        combination_durations = {
            "1-Room HDB, Scandinavian": 1,
            "1-Room HDB, Luxury": 2,
            "1-Room HDB, Modern-Luxury": 3,
            "1-Room HDB, Traditional": 4,
            "1-Room HDB, Contemporary": 5,
            "1-Room HDB, Farmhouse": 6,
            "2-Room HDB, Scandinavian": 7,
            "2-Room HDB, Luxury": 8,
            "2-Room HDB, Modern-Luxury": 9,
            "2-Room HDB, Traditional": 10,
            "2-Room HDB, Contemporary": 11,
            "2-Room HDB, Farmhouse": 12,
            "3-Room HDB, Scandinavian": 13,
            "3-Room HDB, Luxury": 14,
            "3-Room HDB, Modern-Luxury": 15,
            "3-Room HDB, Traditional": 16,
            "3-Room HDB, Contemporary": 17,
            "3-Room HDB, Farmhouse": 18,
            "4-Room HDB, Scandinavian": 19,
            "4-Room HDB, Luxury": 20,
            "4-Room HDB, Modern-Luxury": 21,
            "4-Room HDB, Traditional": 22,
            "4-Room HDB, Contemporary": 23,
            "4-Room HDB, Farmhouse": 24,
            "5-Room HDB, Scandinavian": 25,
            "5-Room HDB, Luxury": 26,
            "5-Room HDB, Modern-Luxury": 27,
            "5-Room HDB, Traditional": 28,
            "5-Room HDB, Contemporary": 29,
            "5-Room HDB, Farmhouse": 30
        }
        # Extract card details from the form
        card_number = request.form.get('card_number')
        expiry_date = request.form.get('expiry_date')
        cvv = request.form.get('cvv')
        cardholder_name = request.form.get('cardholder_name')

        # Simple validation (extend this as per your requirement)
        if len(card_number) != 16:
            flash('Card number must be 16 digits.', 'error')
        elif not expiry_date_valid(expiry_date):  # You need to implement this function
            flash('Invalid expiry date.', 'error')
        elif len(cvv) != 3:
            flash('Invalid CVV.', 'error')
        else:
            project_dict = {}
            db = shelve.open('project.db', 'r')
            project_dict = db['Project']
            db.close()
            project = project_dict.get(id)
            house_type = project.get_house_type()
            house_theme = project.get_house_theme()
            key1 = f"{house_type}, {house_theme}"
            duration_months = combination_durations.get(key1, 0)
            # Calculate total price
            base_price_per_month = 1000
            total_price = duration_months * base_price_per_month
            project.set_total_price(total_price)
            project_list = []
            return redirect(url_for('retrieveProject',email=email))
    return render_template('checkout.html',project= project, id = id , email = email)
@app.route('/retrieveProject')
def retrieveProject():

    email = request.args.get('email')
    combination_durations = {
        "1-Room HDB, Scandinavian": 1,
        "1-Room HDB, Luxury": 2,
        "1-Room HDB, Modern-Luxury": 3,
        "1-Room HDB, Traditional": 4,
        "1-Room HDB, Contemporary": 5,
        "1-Room HDB, Farmhouse": 6,
        "2-Room HDB, Scandinavian": 7,
        "2-Room HDB, Luxury": 8,
        "2-Room HDB, Modern-Luxury": 9,
        "2-Room HDB, Traditional": 10,
        "2-Room HDB, Contemporary": 11,
        "2-Room HDB, Farmhouse": 12,
        "3-Room HDB, Scandinavian": 13,
        "3-Room HDB, Luxury": 14,
        "3-Room HDB, Modern-Luxury": 15,
        "3-Room HDB, Traditional": 16,
        "3-Room HDB, Contemporary": 17,
        "3-Room HDB, Farmhouse": 18,
        "4-Room HDB, Scandinavian": 19,
        "4-Room HDB, Luxury": 20,
        "4-Room HDB, Modern-Luxury": 21,
        "4-Room HDB, Traditional": 22,
        "4-Room HDB, Contemporary": 23,
        "4-Room HDB, Farmhouse": 24,
        "5-Room HDB, Scandinavian": 25,
        "5-Room HDB, Luxury": 26,
        "5-Room HDB, Modern-Luxury": 27,
        "5-Room HDB, Traditional": 28,
        "5-Room HDB, Contemporary": 29,
        "5-Room HDB, Farmhouse": 30
    }
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
        house_type = project.get_house_type()
        house_theme = project.get_house_theme()
        key1 = f"{house_type}, {house_theme}"
        print(f"House Type: {house_type}, House Theme: {house_theme}")
        print(f"Generated Key: {key1}")
        duration_months = combination_durations.get(key1, 0)
        # Debugging prints
        print(f"Combination: {key1}, Duration in months: {duration_months}")
        start_date = project.get_start_date()
        print(f"Start Date: {start_date}")
        end_date = start_date + timedelta(days=duration_months * 30)
        remaining_days = (end_date - start_date).days
        print(f"End Date: {end_date}, Remaining Days: {remaining_days}")
        project.set_remaining_time(remaining_days)
        project_list.append(project)
        print(project_list)
        print(project.get_owner_id())
    return render_template('retrieveProject.html',  project_list=project_list,email=email)

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

@app.route('/projectReview/<int:id>', methods=['POST','GET'])
def project_reviews(id):

    project_dict = {}
    db = shelve.open('project.db', 'r')
    project_dict = db['Project']
    project = project_dict.get(id)
    db.close()
    if request.method == 'POST':
        db = shelve.open('project.db', 'r')
        project_dict = db['Project']
        project = project_dict.get(id)
        db.close()
        file = request.files['image']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        image = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        current_dict = {}
        db = shelve.open('current.db', 'r')
        try:
            current_dict = db['Current']
        except:
            print("Error in retrieving")
        email = current_dict['currentsession']
        db.close()
        print(email)
        rating = starrating(email,request.form.get('review'),request.form.get('rating'),image)
        add_rating(rating)
        rating_dict = {}
        db = shelve.open('rating.db', 'r')
        try:
            rating_dict = db['Rating']
        except:
            print("Error in retrieving Ratings")

        db.close()

        comments = rating.comment_get()
        carousel_items = []
        for rating_id, rating_obj in rating_dict.items():
            image_filename = os.path.basename(rating_obj.get_image())
            web_image_path = image_filename.replace('\\', '/')  # Normalize for web path
            carousel_item = {
                'image': web_image_path,
                'comments': f"projectReview/{id}/{rating_obj.comment_get()}"
            }
            carousel_items.append(carousel_item)

        # testlist = []
        # for ada in rating_dict.items():
        #     image_path = os.path.basename(rating.get_image())
        #     testlist.append(image_path)
        return render_template('about.html',carousel_items =carousel_items,email=email)
    else:
        return render_template('projectReview.html', project=project)

@app.route('/about',methods=['POST','GET'])
def about():
    email = request.args.get('email')
    ratelist = request.args.get('ratelist')

    return render_template('about.html', ratelist=ratelist,email=email)


if __name__ == '__main__':
    app.run(debug=True)
