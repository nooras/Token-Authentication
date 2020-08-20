from flask import flash
from flask import url_for
from flask import Flask, session, render_template, redirect, url_for, request, send_from_directory, escape, redirect
import requests
import yaml
import random   
from forms import RegistrationForm, LoginForm
from models import *
from flask_sqlalchemy import SQLAlchemy
# from wtform_fields import *

ap = Flask(__name__)
ap.config['SECRET_KEY'] = 'kjbjjgcvbjkljhgcvbnkhgf6525125654'

ap.config['SQLALCHEMY_DATABASE_URI'] = "postgres://mqekxcpatpfgcs:1c078f0dcf9fed60350475aea0ad18f8413b4da3d74a4839fc17f88f2263d6a9@ec2-3-208-50-226.compute-1.amazonaws.com:5432/d91kg3fr28it9bxyz"
dbb = SQLAlchemy(ap)

headers = {
    'authorization': "kMfOW74oSHs0NbqDxyidgEVZuBvaCnr2Qcph9t6IlmYGXzJ3TPJsVXpBIYZM3euayObF6wtv9Rlk0rzjxyz",
    'cache-control': "no-cache",
    'content-type': "application/x-www-form-urlencoded"
    }

url = "https://www.fast2sms.com/dev/bulk"

#Updateing Flag variable while registring User
flag = 0
def global_var_change():
    global flag
    if flag == 0:
        flag = 1
    elif flag == 1:
        flag = 0

#Function for otp generation
@ap.route('/sendotp',methods=['POST','GET'])
def sendotp():
    form = RegistrationForm()
    if request.method == 'POST':
        details = request.form
        session['username'] = details['username']
        session['email'] = details['email']
        session['password'] = details['password']
        session['cpassword'] = details['confirm_password']
        num=session['phone'] = request.form['phone']
        verification_code = generate_code()
        session['number'] = verification_code
        # print("Sesssionnnn---",session['number'])
        payload = {'sender_id': 'FSTSMS', 'language':'english','route':'qt','numbers': num, 'message': '33345','variables': '{#AA#}', 'variables_values': verification_code}
        response = requests.request("POST", url, data=payload, headers=headers)
        # print(payload)
        # print(response.text)
        return render_template('confirmotp.html')

#Function for Confirm OTP
@ap.route('/confirmotp',methods=['POST','GET'])
def confirmotp():
    if request.method == 'POST':
        num = request.form['verification']
        print(session['number'])
        if(num == session['number']):
            # print("--->>>",session['number'],num)
            global_var_change()
            # print("InCOnnn",flag)
            return redirect(url_for('register'))
        return render_template('register.html')

#Random code generation for sendotp
def generate_code():
    return str(random.randrange(10000, 99999))

@ap.route('/home')
def home():
    return render_template('home.html')

@ap.route('/',methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if(session.get('number') is not None and flag==1):
        global_var_change()
        details = request.form
        no = int(session['phone'])
        username = session['username']
        email = session['email']
        password = session['password']
        cpassword = session['cpassword']
        user = User(username=username, email=email, phone=no, password=password)
        dbb.session.add(user)
        dbb.session.commit()
        # print("INNNNDEXXXX")
        flash(f'Account created!', 'Success')
        return redirect(url_for('home'))
    return render_template('register.html',title = 'Register',form=form)

#Login for User
@ap.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        email =  request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and (user.password == password): 
            flash('Successfully login.')
            return redirect(url_for('home')) 
        else:
            flash('Email and password in invalid .')
            return render_template('login.html',title = 'Login',form=form)
    return render_template('login.html',title = 'Login',form=form)

if __name__ == '__main__':
    ap.run(port=5004,debug=True)
