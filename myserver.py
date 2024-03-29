from datetime import timedelta

import socketio
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session, send_file, \
    render_template_string
from flask_wtf.csrf import CSRFProtect
from Customers import customer
from Staff import staff
from Forms import *
from Db_functions import *
from werkzeug.utils import *
from User import User
from project import Project
from logincheck import logincheck
from flask_mail import Mail, Message
import os
import uuid
from random import *
import bcrypt
import copy
import pandas as pd
from flask import send_file
from events import socketio

latest_excel_file_path = None

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'supersecretkey'
UPLOAD_FOLDER = os.path.normpath(os.path.join('static', 'image'))
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
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
otp = randint(000000, 999999)


@app.route('/logout')
def logout():
    email = session['email']
    with shelve.open('staff.db', 'w') as db:
        staff_dict = db.get('Staff', {})
        user = staff_dict.get(email)
        if email in staff_dict:
            if session['role'] != "Manager":
                staff_member = staff_dict.get(email)
                staff_member.set_timeout(datetime.now())
                with shelve.open('staff.db', 'w') as db:
                    staff_dict[email] = staff_member  # Update the object in the dictionary
                    db['Staff'] = staff_dict  # Save the updated dictionary back to the database

                print('time out', staff_member.get_timeout())
                session.clear()
                return redirect(url_for('home'))
            else:
                session.clear()
                return redirect(url_for('home'))
        else:
            session.clear()
            return redirect(url_for('home'))


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/verify', methods=['POST', 'GET'])
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
        if otp == int(user_otp):
            return redirect(url_for('resetPassword', email=email))

    return render_template('verifyOTP.html', form=create_otp_form)


@app.route('/resetPassword', methods=['GET', 'POST'])
def resetPassword():
    email = request.args.get('email')
    print(email)
    create_reset_form = resetpassword(request.form)
    if request.method == 'POST' and create_reset_form.validate():

        if create_reset_form.password1.data == create_reset_form.password2.data:
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
                db = shelve.open('staff.db', 'w')
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
    return render_template('landingpage.html')


# login
@app.route('/login', methods=['GET', 'POST'])
def login():
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

                if email in staff_dict:
                    staff_member = staff_dict.get(email)
                    session['user_type'] = 'staff'
                    session['role'] = staff_member.get_role()
                    if staff_member.get_role() != "Manager":
                        staff_member.set_timein(datetime.now())
                        with shelve.open('staff.db', 'w') as db:
                            staff_dict[email] = staff_member  # Update the object in the dictionary
                            db['Staff'] = staff_dict  # Save the updated dictionary back to the database

                        print('time in', staff_member.get_timein())
                        return redirect(url_for('retrieveStaff', email=email))

                    return redirect(url_for('retrieveStaff', email=email))
                else:
                    session['user_type'] = 'customer'
                    return redirect(url_for('retrieveCustomers', email=email))
            else:
                flash("Invalid username or password", "danger")
        else:
            flash("Invalid username or password", "danger")

    is_logged_in = 'email' in session
    return render_template('Startpage.html', form=create_login_form, is_logged_in=is_logged_in)


# Staff CRUD
@app.route("/createStaff", methods={'GET', 'POST'})
def create_staff():
    create_Staff_form = CreateStaffForm(request.form)
    if request.method == 'POST' and create_Staff_form.validate():
        Staff = staff(create_Staff_form.name.data, create_Staff_form.phonenumber.data, create_Staff_form.email.data,
                      create_Staff_form.address.data, create_Staff_form.password.data, create_Staff_form.role.data,
                      datetime.now(), "")
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
            flash('Email already exists!!.')
            print("duplicate email found!")
        else:
            Staff.set_role(create_Staff_form.role.data)
            session['role'] = Staff.get_role()
            session['email'] = Staff.get_email()
            add_staff(Staff)
            Staff.set_timein(datetime.now())
            Staff.set_timeout('')
            staff_dict[Staff.get_email()] = Staff  # Update staff member object in staff_dict
            print(Staff.get_role())
            print("Session role set to:", session['role'])
            print(session['role'])
            print(Staff.get_name(),
                  "was stored in staff.db successfully with user_id ==",
                  Staff.get_id())

        return redirect(url_for('retrieveStaff'))
    return render_template('createStaff.html', form=create_Staff_form)


@app.route("/retrieveStaff")
def retrieveStaff():
    email = session['email']
    role = session['role']
    staff_dict = {}
    db = shelve.open('staff.db', 'r')
    staff_dict = db['Staff']
    db.close()
    staff_list = []
    if email in staff_dict:
        staff = staff_dict.get(email)
        staff_list.append(staff)
    if role == 'Manager':
        print('I am a manager')

    if role == 'Senior Consultant':
        print('I am senior consultant')

    if role == 'Consultant':
        print("I am a consultant")

    return render_template('retrieveStaff.html', count=len(staff_list), staff_list=staff_list)


@app.route('/manageProject')
def manageProject():
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
    email = session['email']
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
    return render_template('manageProject.html', project_list=project_list, email=email)


@app.route('/updateProject/<int:id>/', methods=['GET', 'POST'])
def update_Project(id):
    update_customer_form = update_Project_form(request.form)

    if request.method == 'POST' and update_customer_form.validate():
        project_dict = {}
        db = shelve.open('project.db', 'w')
        project_dict = db['Project']

        # Check if the customer exists in the dictionary
        if id in project_dict:
            Project = project_dict[id]
            Project.set_address(request.form['address'])
            Project.set_phone(request.form['phone'])
            Project.set_house_type(request.form['house_type'])
            Project.set_house_theme(request.form['house_theme'])
            Project.set_comments(request.form['comments'])
            Project.set_status(request.form['status'])

            db['Project'] = project_dict
            db.close()
            flash('Customer updated successfully', 'success')
        return redirect(url_for('manageProject'))

    else:
        project_dict = {}
        db = shelve.open('project.db', 'r')
        project_dict = db['Project']
        db.close()
        # Check if the customer exists in the dictionary
        if id in project_dict:
            Project = project_dict[id]

            print('hello')
            return render_template('updateProject.html', form=update_customer_form)

        flash('Customer not found', 'error')
    return redirect(url_for('updateProject'))


@app.route("/managestaff")
def managestaff():
    # Make sure the user is logged in
    email = session.get('email')
    if not email:
        # Redirect to the login page if not logged in
        return redirect(url_for('login'))

    # Open the database and retrieve staff data
    staff_dict = {}
    db = shelve.open('staff.db', 'r')
    staff_dict = db.get('Staff', {})
    db.close()

    # Create a list for staff, excluding managers
    staff_list = []
    for key in staff_dict:
        staff_member = staff_dict.get(key)
        # Add staff members who are not managers
        if staff_member.get_role().lower() != 'manager':
            # Format timein and timeout
            timein = staff_member.get_timein()
            timeout = staff_member.get_timeout()
            if timein:
                staff_member.timein_formatted = timein.strftime("%Y:%m:%d: %H:%M:%S")
            else:
                staff_member.timein_formatted = "Not Set"

            if timeout:
                staff_member.timeout_formatted = timeout.strftime("%Y:%m:%d: %H:%M:%S")
            else:
                staff_member.timeout_formatted = "Not Set"

            staff_list.append(staff_member)
            print("My time in", staff_member.get_timein())
            print("My time out", staff_member.get_timeout())
            print(staff_member)
        print(staff_list)

    # Render the managestaff template with the staff list
    return render_template('managestaff.html', count=len(staff_list), staff_list=staff_list)


@app.route("/updateStaff/<string:email>/", methods=['GET', 'POST'])
def updateStaff(email):
    update_staff_form = UpdateStaffForm(request.form)

    if request.method == 'POST' and update_staff_form.validate():
        staff_dict = {}
        db = shelve.open('staff.db', 'w')
        staff_dict = db['Staff']

        # Check if the staff exists in the dictionary
        if email in staff_dict:
            Staff = staff_dict[email]
            Staff.set_name(update_staff_form.name.data)
            print(update_staff_form.password.data)
            passwordhash = update_staff_form.password.data
            password2 = hash_password(passwordhash)

            Staff.set_password(password2)

            try:
                file = request.files['image']
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            except:
                image = 'default'
            if image == "default":
                Staff.set_image("default")
            else:
                Staff.set_image(image)
                print(Staff.get_image())

            Staff.set_email(update_staff_form.email.data)
            db['Staff'] = staff_dict
            db.close()
            flash('Staff updated successfully', 'success')
            return redirect(url_for('retrieveStaff', email=email))

    else:
        staff_dict = {}
        db = shelve.open('staff.db', 'r')
        staff_dict = db['Staff']
        db.close()

        # Check if the staff exists in the dictionary
        if email in staff_dict:
            Staff = staff_dict[email]
            update_staff_form.name.data = Staff.get_name()
            update_staff_form.email.data = Staff.get_email()
            update_staff_form.password.data = Staff.get_password()
            return render_template('updateStaff.html', form=update_staff_form, email=email)

    flash('Staff not found', 'error')
    return redirect(url_for('updateStaff'))


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
@app.route("/createblog", methods=['GET', 'POST'])
def UploadImage():
    email = request.args.get('email')
    if request.method == 'POST':
        files = request.files.getlist('image[]')  # To handle multiple files
        name = request.form['name']
        comment = request.form['comment']
        creator = session['email']
        # Initialize a list to hold the filenames for saving and later reference
        filenames = []

        try:
            for file in files:
                if file:  # Ensure a file is present
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)
                    # Store just the filename or a relative path as needed
                    filenames.append(filename)

            # Create a new blog instance
            Blog = blog(name, comment, filenames, creator)  # Directly pass the list of filenames

            add_blog(Blog)  # Assuming this function adds the blog to your database or storage
            print(Blog.get_blog_image())
            # No need to call set_blog_image if the __init__ method already handles image setting
            # However, if additional image processing is required, you can call it here

            # Retrieve image information for redirection or rendering
            fileimages = Blog.get_blog_image()  # This will now return a list of image filenames

            # Render a template or redirect as needed
            # Passing 'fileimages' as a list of filenames to the template or redirect URL
            return redirect(url_for('about', name=name, comment=comment))

        except Exception as e:
            flash('An error occurred: {}'.format(e))

    return render_template('createBlog.html')


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
    session['blog_list'] = blog_list
    print(session['blog_list'])

    return render_template('about.html', count=len(blog_list), blog_list=blog_list, Ccounter=len(Customer_list),
                           Customer_list=Customer_list, email=email)


@app.route('/viewblog/<int:id>')
def viewblog(id):
    blog_list = session.get('blog_list', [])
    blog = next((item for item in blog_list if item['id'] == id), None)
    db = shelve.open('blog.db', 'r')
    blog_dict = db.get('Blog', {})
    db.close()
    blog = blog_dict[id]
    if blog:
        images = blog.get_blog_image()
        session['images'] = images
        print(images)
        print(blog.get_blog_id())
        form = UpdateBlogForm()  # Create an instance of the form to pass to the template
        return render_template('ViewBlog.html', blog=blog, images=images, form=form)
    else:
        return "Blog not found", 404


@app.route('/updateblog/<int:id>/', methods=['GET', 'POST'])
def update_blog(id):
    email = request.args.get('email')

    db = shelve.open('blog.db', 'w')
    blog_dict = db.get('Blog', {})

    if id not in blog_dict:
        db.close()
        flash('Blog not found', 'error')
        return redirect(url_for('retrieveblog'))

    blog = blog_dict[id]
    Update_blog_form = UpdateBlogForm(obj=blog)

    if request.method == 'POST' and Update_blog_form.validate():
        # Update title and content
        blog.set_name(Update_blog_form.name.data)
        blog.set_comment(Update_blog_form.comment.data)

        # Handle image updates
        images_to_remove = request.form.getlist('images_to_remove')
        updated_images = update_blog_images(request.files.getlist('image'), blog.get_blog_image(), images_to_remove)

        if updated_images is not None:
            blog.set_blog_image(updated_images)

        blog_dict[id] = blog
        db['Blog'] = blog_dict
        db.close()
        flash('Blog updated successfully', 'success')
        return redirect(url_for('retrieveblog'))

    db.close()
    existing_images = blog.get_blog_image()
    return render_template('updateBlog.html', form=Update_blog_form, id=id, email=email,
                           existing_images=existing_images)


@app.route('/update_blog_field/<int:id>', methods=['POST'])
def update_blog_field(id):
    field = request.form.get('field')  # Get the field name
    value = request.form.get('value')  # Get the value
    db = shelve.open('blog.db', 'w')  # Open the shelve database in write mode
    blog_dict = db.get('Blog', {})

    try:
        if id in blog_dict:
            blog = blog_dict[id]
            if field == 'name':
                blog.set_name(value)
            elif field == 'comment':
                blog.set_comment(value)
            blog_dict[id] = blog  # Update the blog in the dictionary
            db['Blog'] = blog_dict  # Save the updated dictionary back to the database
            print(blog_dict)
            print(blog.get_name())
            print(blog.get_comment())
            return jsonify({"field": field, "value": value}), 200
        else:
            return 'Blog not found', 404
    finally:
        db.close()  # Ensure the database is closed properly


@app.route('/upload_blog_images/<int:id>', methods=['POST'])
def upload_blog_images(id):
    db = shelve.open('blog.db', 'w')
    blog_dict = db.get('Blog', {})
    blog = blog_dict.get(id)
    blog = blog_dict[id]
    if not blog:
        db.close()
        return jsonify({"message": "Blog not found"}), 404

    # No images to remove on a fresh upload, so pass an empty list
    images_to_remove = []
    uploaded_files = request.files.getlist('images')
    existing_images = blog.get_blog_image() if blog.get_blog_image() else []

    # Call the update function to process the images
    updated_images = update_blog_images(uploaded_files, existing_images, images_to_remove)

    if updated_images is not None:
        blog.set_blog_image(updated_images)
        blog_dict[id] = blog
        db['Blog'] = blog_dict
        db.close()
        print(blog.get_blog_image())
        return jsonify({"message": "Images uploaded successfully"}), 200
    else:
        db.close()
        return jsonify({"message": "An error occurred while updating images"}), 500


def update_blog_images(uploaded_files, existing_images, images_to_remove):
    # Retain existing images not marked for removal and add new images
    filenames = [img for img in existing_images if img not in images_to_remove]

    for file in uploaded_files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            filenames.append(filename)

    return filenames


@app.route('/delete_blog_images/<int:id>', methods=['POST'])
def delete_blog_images(id):
    image_names_to_remove = request.form.getlist('images_to_remove')
    print(f"Requested images to remove: {image_names_to_remove}")

    with shelve.open('blog.db', writeback=True) as db:
        blog_dict = db.get('Blog', {})

        if id not in blog_dict:
            print(f"Blog with ID {id} not found.")
            return jsonify({"error": "Blog not found"}), 404

        blog = blog_dict[id]

        # Remove specified images using the new method
        updated_images_after_removal = blog.remove_blog_images(image_names_to_remove)
        print(f"Images after removal: {updated_images_after_removal}")

        # Delete specified images from the filesystem
        for img_to_remove in set(image_names_to_remove):
            file_path = os.path.join('static/image/', img_to_remove)
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    print(f"Deleted image {file_path}.")
                else:
                    print(f"File {file_path} not found.")
            except OSError as e:
                print(f"Error deleting image {img_to_remove}: {e.strerror}")

        # Sync the updated blog data to the database
        db['Blog'] = blog_dict
        db.sync()

    # Retrieve the final updated list of images for response
    final_updated_images = blog.get_blog_images()
    print("Final updated images in blog object:", final_updated_images)

    return jsonify({"message": "Images deleted successfully", "remainingImages": final_updated_images})

@app.route('/deleteblog/<int:id>', methods=['POST'])
def deleteblog(id):
    # Open the shelve database
    db = shelve.open('blog.db', 'c')  # Use 'c' for read/write access, create if necessary
    try:
        blog_dict = db['Blog']
        if id in blog_dict:
            # Retrieve the current user's email or ID from the session
            current_user_id = session.get('email')  # Adjust if you use another identifier than email
            blog_post = blog_dict[id]

            # Use the correct getter to check the creator's identity
            if blog_post.get_creator() == current_user_id:
                del blog_dict[id]
                db['Blog'] = blog_dict
                flash('Blog post deleted successfully.')
            if session['user_type'] == 'staff':
                del blog_dict[id]
                db['Blog'] = blog_dict
                flash('Blog post deleted successfully.')
            else:
                flash('You do not have permission to delete this blog post.')
        else:
            flash('Blog post not found.')
    except KeyError:
        flash('No blog data found.')
    finally:
        db.close()

    return redirect(url_for('about'))

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
        email = Customer.get_email()
        if Customer.get_email() in staff_dict or Customer.get_email() in customer_dict:
            print("same email!")
            flash('Email already exists!!.')
        else:
            add_customer(Customer)
            print(Customer.get_first_name(), Customer.get_last_name(),
                  "was stored in customer.db successfully with user_id ==",
                  Customer.get_customer_id())

            return redirect(url_for('retrieveCustomers', email=email))

    return render_template('createCustomer.html', form=create_Customer_form)


@app.route('/retrieveCustomers')
def retrieveCustomers():
    email = request.args.get('email')
    customer_dict = {}
    db = shelve.open('customer.db', 'r')
    customer_dict = db['Customer']
    db.close()

    Customer_list = []
    if email in customer_dict:
        customer = customer_dict.get(email)
        Customer_list.append(customer)

    rating_dict = {}
    db = shelve.open('rating.db', 'c')
    try:
        rating_dict = db['Rating']
    except:
        print("Error in retrieving")

    ratinglist = []
    for rating in rating_dict:
        rating2 = rating_dict.get(rating)
        if email == rating2.email_get():
            ratinglist.append(rating2)

    db.close()

    return render_template('retrieveCustomer.html', count=len(Customer_list), Customer_list=Customer_list, email=email,
                           countre=len(ratinglist), ratinglist=ratinglist)


@app.route('/updateCustomer/<string:email>/', methods=['GET', 'POST'])
def update_user(email):
    update_customer_form = UpdateCustomerForm(request.form)
    if request.method == 'POST' and update_customer_form.validate():
        try:
            db = shelve.open('customer.db', 'w')
            customer_dict = db.get('Customer', {})

            # Check if the customer exists in the dictionary
            if email in customer_dict:
                customer = customer_dict[email]
                customer.set_first_name(update_customer_form.first_name.data)
                customer.set_last_name(update_customer_form.last_name.data)

                # Handle password update, if provided
                if update_customer_form.password.data:
                    password_hash = hash_password(update_customer_form.password.data)
                    customer.set_password(password_hash)

                # Handle image upload
                file = request.files.get('image')
                if file and file.filename != '':  # Check if a file is uploaded
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)
                    customer.set_image(file_path)
                else:  # If no new image is uploaded, keep the current image
                    customer.set_image(customer.get_image())

                customer.set_email(update_customer_form.email.data)

                # Update the customer_dict with the modified customer
                customer_dict[email] = customer
                db['Customer'] = customer_dict
            else:
                flash('Customer not found', 'error')
                return redirect(url_for('retrieveCustomers'))
        except Exception as e:
            flash('An error occurred: ' + str(e), 'error')
            return redirect(url_for('updateCustomers'))
        finally:
            db.close()
        flash('Customer updated successfully', 'success')
        return redirect(url_for('retrieveCustomers', email=email))
    elif request.method == 'GET':
        try:
            db = shelve.open('customer.db', 'r')
            customer_dict = db.get('Customer', {})

            # Check if the customer exists in the dictionary
            if email in customer_dict:
                customer = customer_dict[email]
                update_customer_form.first_name.data = customer.get_first_name()
                update_customer_form.last_name.data = customer.get_last_name()
                update_customer_form.email.data = customer.get_email()
            else:
                flash('Customer not found', 'error')
                return redirect(url_for('updateCustomers'))
        except Exception as e:
            flash('An error occurred: ' + str(e), 'error')
            return redirect(url_for('updateCustomers'))
        finally:
            db.close()
        return render_template('updateCustomer.html', form=update_customer_form, email=email)

    flash('Customer not found', 'error')
    return redirect(url_for('updateCustomers'))
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
        return redirect(url_for('checkout', id=id, email=email))

    return render_template('projectSummary.html', project=project, id=id, email=email)


@app.route('/checkout/<int:id>/', methods=['GET', 'POST'])
def checkout(id):
    def expiry_date_valid(expiry_date):
        try:
            exp_date = datetime.strptime(expiry_date, "%m/%y")
            return exp_date > datetime.now()
        except ValueError:
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

        if len(card_number) != 16:
            flash('Card number must be 16 digits.', 'error')
        elif not expiry_date_valid(expiry_date):
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
            db = shelve.open('project.db', 'w')
            db['Project'] = project_dict
            db.close()
            project_list = []
            return redirect(url_for('retrieveProject', email=email))
    return render_template('checkout.html', project=project, id=id, email=email)


@app.route('/retrieveProject')
def retrieveProject():
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
    email = session['email']
    project_list = []
    for key in project_dict:
        project = project_dict.get(key)

        if project.get_email() == session['email']:
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
    return render_template('retrieveProject.html', project_list=project_list, email=email)


@app.route('/createProject2', methods=['GET', 'POST'])
def create_Project2():
    email = request.args.get('email')
    create_project_form = CreateProject(request.form)
    if request.method == 'POST':
        project = Project(create_project_form.address.data, create_project_form.phone.data,
                          create_project_form.house_type.data,
                          create_project_form.house_theme.data, create_project_form.comments.data)
        email = session['email']
        print(session['email'], 'thiis is session email')
        print(email, 'IT IS STORED??')
        project.set_email(email)
        add_project(project)
        print(project.get_owner_id())
        project.set_start_date(datetime.now())
        print(project.get_email(), 'IT IS STORED?? whyyyy')
        print(project.get_email())
        print(project.get_start_date())
        print(project.get_phone(), "was stored in project.db successfully with project_id ==", project.get_owner_id())
        print(project)
        id1 = project.get_owner_id()
        return redirect(url_for('projectSummary', id=id1, project=project, email=email))

    return render_template('createProject2.html', form=create_project_form, email=email)


@app.route('/deleteProject/<int:id>', methods=['POST'])
def delete_project(id):
    project_dict = {}
    db = shelve.open('project.db', 'w')
    project_dict = db['Project']
    project_dict.pop(id)
    db['Project'] = project_dict
    db.close()
    return redirect(url_for('retrieveProject'))


@app.route('/projectReview/<int:id>', methods=['POST', 'GET'])
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
        try:
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
            rating = starrating(email, request.form.get('review'), request.form.get('rating'), image)
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
            session['carousel_items'] = carousel_items
            return redirect(url_for('about'))
        except:
            flash('File cannot be empty!!!!!!!')

    return render_template('projectReview.html', project=project)


@app.route('/about', methods=['POST', 'GET'])
def about():
    print("Entered about route")
    page = request.args.get('page', 1, type=int)
    per_page = 9
    search_query = request.args.get('search', '').lower()  # Get search query and convert to lowercase
    email = request.args.get('email', default='')  # Assuming email is optional
    ratelist = request.args.get('ratelist', default='')  # Assuming ratelist is optional
    carousel_items = request.args.get('carousel_items', default='')
    db = shelve.open('blog.db', 'r')
    blog_dict = db['Blog']
    db.close()

    # Filter blogs based on search query
    if search_query:
        filtered_blog_dict = {k: v for k, v in blog_dict.items() if
                              search_query in v.get_name().lower() or search_query in v.get_comment().lower()}
    else:
        filtered_blog_dict = blog_dict

    # Calculate total pages
    total_blogs = len(filtered_blog_dict)
    total_pages = (total_blogs + per_page - 1) // per_page
    print(total_pages)

    # Create paginated blog_list
    blog_list = []
    sorted_keys = sorted(filtered_blog_dict.keys())[(page - 1) * per_page: page * per_page]
    for key in sorted_keys:
        blog = filtered_blog_dict[key]
        blog_images = blog.get_blog_image()

        # Ensure blog_images is a list
        if not isinstance(blog_images, list):
            blog_images = [blog_images]  # Wrap single image in a list for consistency

        web_image_paths = []
        for image in blog_images:
            if image:
                image_filename = os.path.basename(image)
                web_image_path = image_filename.replace('\\', '/')
                web_image_paths.append(web_image_path)

        blog_item = {
            'id': blog.get_blog_id(),
            'images': web_image_paths,  # Now a list of image paths
            'title': blog.get_name(),
            'content': blog.get_comment(),
        }
        blog_list.append(blog_item)
        session["blog_list"] = blog_list
    print("Total Pages:", total_pages)
    # Retrieve carousel_items from session
    carousel_items = session.get('carousel_items', [])
    session['blog_list'] = blog_list
    # Check if it's an AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_template('partials/blog_list.html', blog_list=blog_list)
        return jsonify({'html': html, 'totalPages': total_pages})
    else:
        return render_template('about.html', email=email, ratelist=ratelist, blog_list=blog_list,
                               total_pages=total_pages,
                               current_page=page, carousel_items=carousel_items)


@app.route('/verify_password/<string:email>/', methods=['POST'])
def verify_password(email):
    entered_password = request.form['password']
    db = shelve.open('customer.db', 'r')
    customer_dict = db['Customer']
    db.close()

    user = customer_dict.get(email)
    print(entered_password.encode('utf-8'))
    print(user.get_password())
    if user and bcrypt.checkpw(entered_password.encode('utf-8'), user.get_password()):
        return redirect(url_for('update_user', email=email))
    else:
        flash('Incorrect password', 'error')

        customer_dict = {}
        db = shelve.open('customer.db', 'r')
        customer_dict = db['Customer']
        db.close()

        Customer_list = []
        if email in customer_dict:
            customer = customer_dict.get(email)
            Customer_list.append(customer)

        rating_dict = {}
        db = shelve.open('rating.db', 'c')
        try:
            rating_dict = db['Rating']
        except:
            print("Error in retrieving")

        ratinglist = []
        for rating in rating_dict:
            rating2 = rating_dict.get(rating)
            if email == rating2.email_get():
                ratinglist.append(rating2)

        db.close()
        return render_template('retrieveCustomer.html', count=len(Customer_list), Customer_list=Customer_list,
                               email=email, countre=len(ratinglist), ratinglist=ratinglist, error=True)


@app.route('/verify_passwordstaff/<string:email>/', methods=['POST'])
def verify_passwordstaff(email):
    entered_password = request.form['password']
    db = shelve.open('staff.db', 'r')
    staff_dict = db['Staff']
    db.close()

    user = staff_dict.get(email)
    print(user)
    print(entered_password.encode('utf-8'))
    print(user.get_password())
    if user and bcrypt.checkpw(entered_password.encode('utf-8'), user.get_password()):
        return redirect(url_for('updateStaff', email=email))
    else:
        flash('Incorrect password', 'error')

        staff_dict = {}
        db = shelve.open('staff.db', 'r')
        staff_dict = db['Staff']
        db.close()

        Staff_list = []
        if email in staff_dict:
            staff = staff_dict.get(email)
            Staff_list.append(staff)

        rating_dict = {}
        db = shelve.open('rating.db', 'c')
        try:
            rating_dict = db['Rating']
        except:
            print("Error in retrieving")

        ratinglist = []
        for rating in rating_dict:
            rating2 = rating_dict.get(rating)
            if email == rating2.email_get():
                ratinglist.append(rating2)

        db.close()
        return render_template('retrieveStaff.html', count=len(Staff_list), staff_list=Staff_list,
                               email=email, countre=len(ratinglist), ratinglist=ratinglist, error=True)


@app.route('/report/', methods=['POST', 'GET'])
def generateReport():
    global latest_excel_file_path
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
    project_list = []

    # Open the shelve database and retrieve project data
    with shelve.open('project.db', 'r') as db:
        project_dict = db.get('Project', {})
        for project in project_dict.values():
            project_list.append(project)

    if project_list:
        projects_data = [{
            "Address": project.get_address(),
            "Phone": project.get_phone(),
            "House Type": project.get_house_type(),
            "House Theme": project.get_house_theme(),
            "Comments": project.get_comments(),
            "Start Date": project.get_start_date().strftime("%Y-%m-%d"),
            "Total Price": project.get_total_price(),
            "Email": project.get_email(),
            "Status": project.get_status()
        } for project in project_list]
        print(project_list, 'tis the list\n')
        print(projects_data, 'this the file')
        df = pd.DataFrame(projects_data)
        datetime_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        excel_file_name = f'Report_{datetime_str}.xlsx'
        excel_file_path = os.path.join('static/temp_reports/', excel_file_name)

        # Ensure the directory exists
        os.makedirs(os.path.dirname(excel_file_path), exist_ok=True)

        # Save DataFrame to Excel
        df.to_excel(excel_file_path, index=False, engine='openpyxl')
        latest_excel_file_path = excel_file_path
        # Redirect to another page after saving the file
        return redirect(url_for('get_latest_report'))
    else:
        latest_excel_file_path = None
        # Render a simple message if there are no projects
        return render_template_string('<p>No projects found for the current user.</p>')


@app.route('/get-latest-report')
def get_latest_report():
    global latest_excel_file_path
    if latest_excel_file_path:
        file_url = latest_excel_file_path
        return render_template('dashboard.html', file_url=file_url)
    else:
        return "No report available", 404


@app.route('/staff_reply')
def staff_reply():
    return render_template('staff_reply.html')


def create_app():
    app = Flask(__name__, static_url_path='/static')
    app.config['SECRET_KEY'] = 'supersecretkey'
    UPLOAD_FOLDER = os.path.normpath(os.path.join('static', 'image'))
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
    socketio.init_app(app)
    return app


if __name__ == '__main__':
    app.run(debug=True)
