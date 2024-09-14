from flask import Flask, render_template, request, url_for, redirect, flash,session,send_file, jsonify
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
import os
import re
app = Flask(__name__)
# DATABASE CONFIGURATION
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'automotives'
app.config['UPLOAD_FOLDER'] = 'static/images'

mysql = MySQL(app)
# Set upload folder for images
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create upload folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
@app.route('/submit', methods=['POST'])
def submit_form():
    if request.method=='POST':
        Carname = request.form['Carname']
        Cardetails = request.form['Cardetails']
        Cartype=request.form['Cartype']
        Carimg= request.files['Carimg']
        # Save image file
        filename = secure_filename(Carimg.filename)
        Carimg.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Create a cursor object
        cur = mysql.connection.cursor()

        # Save car details to MySQL database
        query = ("INSERT INTO cars "
                 "(Carname, Cardetails, carimg,Cartype) "
                 "VALUES (%s, %s, %s,%s)")
        data = (Carname, Cardetails, filename, Cartype)  # Provide four values here
        cur.execute(query, data)
        mysql.connection.commit()
        # Get the ID of the newly inserted row
        car_id = cur.lastrowid
        # Save the image data to the MySQL database
        with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'rb') as f:
            image_data = f.read()
        query = ("UPDATE cars SET Carimg= %s WHERE car_id = %s")
        data = (image_data, car_id)
        cur.execute(query, data)
        mysql.connection.commit()
        return jsonify({'message': 'Car details submitted successfully!'})
    if request.method=='POST':
        Carname = request.form['Carname']
        Cardetails = request.form['Cardetails']
        Cartype=request.form['Cartype']
        Carimg= request.files['Carimg']

        # Save image file
        filename = secure_filename(Carimg.filename)
        Carimg.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Create a cursor object
        cur = mysql.connection.cursor()

        # Save car details to MySQL database
        query = ("INSERT INTO cars "
                 "(Carname, Cardetails, carimg,Cartype) "
                 "VALUES (%s, %s, %s,%s)")
        data = (Carname, Cardetails, filename)
        cur.execute(query, data)
        mysql.connection.commit()

        # Get the ID of the newly inserted row
        car_id = cur.lastrowid

        # Save the image data to the MySQL database
        with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'rb') as f:
            image_data = f.read()
        query = ("UPDATE cars SET Carimg_data = %s WHERE car_id = %s")
        data = (image_data, car_id)
        cur.execute(query, data)
        mysql.connection.commit()

        return jsonify({'message': 'Car details submitted successfully!'})
    if request.method=='POST':
     Carname = request.form['Carname']
     Cardetails = request.form['Cardetails']
     Cartype=request.form['Cartype']
     Carimg= request.files['Carimg']

    # Save image file
    filename = secure_filename(Carimg.filename)
    Carimg.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    # Save car details to MySQL database
    query = ("INSERT INTO cars ""(Carname, Cardetails, carimg,Cartype) ""VALUES (%s, %s, %s,%s)")
    data = (Carname, Cardetails, filename)
    cursor.execute (query, data)
    cnx.commit()

    # Get the ID of the newly inserted row
    car_id = cursor.lastrowid

    # Save the image data to the MySQL database
    with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'rb') as f:image_data = f.read()
    query = ("UPDATE cars SET Carimg_data = %s WHERE car_id = %s")
    data = (image_data, car_id)
    cursor.execute(query, data)
    cnx.commit()
    flash('failed! login is required')

@app.route('/all')
def all():
    return render_template('search_results.html')
@app.route('/serve_image/uploads')
def serve_image(uploads):
    return send_file(f'static/images/{uploads}', mimetype='image/jpeg')
@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        value = request.form['value']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM cars WHERE Carname LIKE %s OR Cardetails LIKE %s OR Carimg LIKE %s", ('%' + value + '%', '%' + value + '%', '%' + value + '%'))
        data = cur.fetchall()
        cur.close()
        return render_template('search_results.html', cars=data)

@app.route('/admin')
def admin():
    if 'user_id' in session : 
     cur=mysql.connection.cursor()
     cur.execute('SELECT * FROM cars')
     data=cur.fetchall()
     cur.close()
     return render_template('admin.html',cars=data)
    else :
        flash('failed! login is required')
        return redirect(url_for('login'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login_user',methods=['POST'])
def login_user():
    if request.method=='POST':
        fullname=request.form['fullname']
        email=request.form['email']
        password=request.form['password']
        cur=mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE fullname=%s AND email=%s AND password =%s",( fullname,email,password))
        user=cur.fetchone()
        cur.close()
        #checking existence
        
        if user:
            session['user_id']=user[0]
            session['user_name']=user[1]
            return redirect(url_for('admin'))
        if not(fullname and email and password):
         flash('all fields are essential!')
         return redirect(url_for('login'))
        if not(len(fullname))>=3 and len(email)>=3 and len (password)>=3:
             flash("error logging in! please try again.")
             return redirect(url_for('login'))
        else:
            flash('invalid credentials')
            return redirect(url_for('login'))
    if user:
            session['user_id']=user[0]
            session['user_name']=user[1]
            return redirect(url_for('admin'))
    
    else:
            flash("login success!")
            return redirect(url_for('login'))
            
    #logout 
@app.route('/logout',methods=['POST'])
def logout():
    session.pop('user_id',None)
    session.pop('user_name',None)
    return redirect(url_for('login'))

#delete
@app.route('/delete', methods=['POST'])
def delete():
    if request.method=='POST':
            id=request.form['id']
            cur=mysql.connection.cursor()
            cur.execute("""DELETE FROM cars WHERE id=%s""", (id))
            mysql.connection.commit()
            flash("success! one record deleted")
            return redirect(url_for('main'))    


app.secret_key = 'many random bytes'
@app.route('/update',methods=['POST'])
def update(): 
    if request.method=="POST":
        flash("Data updated successfully")
        id=request.form["id"]
        carname = request.form['Carname']
        cartype = request.form['Cartype']
        cardetails = request.form['Cardetails']
        carimg = request.files['Carimg']

        cur=mysql.connection.cursor()
        cur.execute(""" UPDATE cars SET Carname=%s,Cartype=%s,Cardetails=%s,Carimg=%s WHERE id=%s""",(carname,cartype,cardetails,carimg,id))
        mysql.connection.commit()
        return redirect(url_for("main"))

    


#VALIDATION PHONENUMBER 
def is_valid_phone(phone):
    pattern = r'^\+?254\d{9,16}$'
    return bool(re.match(pattern,phone))
#VALIDATE EMAIL ADDRESS
def is_valid_email(email):
    pattern= r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern,email)
def is_valid_message(message):
    return len(message) >= 10 
 
@app.route('/newsletter')
def newsletter():
    # code to handle the newsletter route
    return render_template('newsletter.html')

@app.route('/subscribe', methods=['POST'])
def subscribe():
    if request.method == 'POST':
        email = request.form.get('email')  # Use get() to avoid KeyError
        # Validate email
        if not email:
            flash("Email required!")
            return redirect(url_for('index'))
        if len(email) < 3:
            flash("Email must be greater than 3")
            return redirect(url_for('index'))
        if not is_valid_email(email):
            flash("Email address format is invalid")
            return redirect(url_for('index'))

        # Check for duplicate entries
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM subscribers WHERE email=%s", (email,))
        subscribers = cur.fetchone()
        cur.close()

        if subscribers:
            flash("Duplicate entries")
            return redirect(url_for('index'))
        # Insert email into database
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO subscribers(email) VALUES(%s)", (email,))
        mysql.connection.commit()
        cur.close()
        flash("subscribed successfully")
        return redirect(url_for('index'))
#INSERT
@app.route('/enter',methods=['POST'])
def enter():
   if request.method=='POST':
       #flash('Thanks you for contacting me')
       name=request.form['fullname']
       phone=request.form['phonenumber']
       email=request.form['email']
       message=request.form['message']
       #check for duplicates
       cur=mysql.connection.cursor()
       cur.execute("SELECT * FROM contacts WHERE phonenumber=%s OR email=%s",(phone,email))
       contact=cur.fetchone()
       cur.close()
       if not(contact):
            if not(name and email and phone and message):
                flash("All fields are required")
                return redirect(url_for('contact'))
            if not(len(name)>=3 and len(email)>=3 and len(phone)>=3 and len(message)>=0):
                flash("Textfield values must greater than or equall to three")
                return redirect(url_for('contact')) 
            if not phone.isdigit():
                flash("The phonenumber must be numeric")
                return redirect(url_for('contact'))
            if not is_valid_phone(phone):
                flash("The phonenumber format is invalid")
                return redirect(url_for('contact'))
            if not is_valid_email(email):
                flash("Email address format is invalid")
                return redirect(url_for('contact'))
            if not is_valid_message(message):
                flash("Message too short!")
                return redirect(url_for('contact'))       
            else:
                    cur=mysql.connection.cursor()
                    cur.execute("INSERT INTO contacts(fullname,phonenumber,email,message) VALUES(%s,%s,%s,%s)",(name,phone,email,message))
                    mysql.connection.commit()
                    flash("Message sent successfully")
                    return redirect(url_for('contact'))
       else:
           flash("Duplicate entries")
           return redirect(url_for('contact'))



@app.route('/')
def index():
     cur=mysql.connection.cursor()
     cur.execute('SELECT * FROM cars')
     data=cur.fetchall()
     cur.close()
     return render_template('index.html',cars=data)
@app.route('/available')
def available():
    return render_template('available.html')
@app.route('/contact')
def contact():
    return render_template('contact.html')
@app.route('/tradeins')
def tradeins():
    return render_template('tradeins.html')
@app.route('/add')
def add():
    return render_template('add.html')
@app.route('/addcars') 
def addcars():
    return render_template('add.html')




if __name__ == '__main__':
    app.run(debug=True)