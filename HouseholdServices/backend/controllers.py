from flask import Flask,render_template,request
from flask import current_app as app
from .models import *


@app.route("/")                                                   
def home():
  return render_template("home.html")


@app.route("/login",methods=["GET","POST"])                        
def login():
  if(request.method == "POST"):
    user_name = request.form.get("uname")
    password = request.form.get("pwd")
    customer = Customer.query.filter_by(user_name = user_name).first()
    service = Services.query.all()
    if(customer):
      if(password != customer.password):
        return render_template("login.html",msg2="Incorrect Password")
      else:
        return render_template("user_dashboard.html",user_name = customer.customer_name,service=service)
    else:
      return render_template("login.html",msg1="User name does not exist.")
  return render_template("login.html")


@app.route("/register",methods=["GET","POST"])                      
def signup():
  if(request.method == "POST"):
    email = request.form.get("email")
    customer_name = request.form.get("full_name")
    user_name = request.form.get("uname")
    password = request.form.get("pwd")
    customer = Customer.query.filter_by(user_name = user_name).first()
    
    if(customer is None):
      new_customer = Customer(user_name=user_name,customer_name=customer_name,email=email,password=password)
      db.session.add(new_customer)
      db.session.commit()
    else:
      return render_template("signup.html",msg="User already exist")
  return render_template("signup.html")

# @app.route("/add",methods=["GET","POST"])
# def add_service():
#   pass

# @app.route("/add",methods=["GET","POST"])
# def edit_service():

# @app.route("/add",methods=["GET","POST"])
# def delete_service():

