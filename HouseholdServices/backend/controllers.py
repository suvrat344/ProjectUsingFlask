from flask import Flask,render_template,request
from flask import current_app as app
from datetime import datetime
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
        return render_template("user_dashboard.html",customer_name = customer.customer_name,customer_id=customer.customer_id,service=service)
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


@app.route("/add_service/<int:customer_id>/<int:service_id>",methods=["GET","POST"])
def add_service(customer_id,service_id):
  '''
    Add new service requested by the customer.
  '''
  
  # Filter out service requested by the customer
  service = Services.query.filter_by(service_id = service_id).first()
  if(request.method == "POST"):
    # Fetch data from service_request.html and convert date into python date object
    request_date = datetime.strptime(request.form.get("request_date"),"%Y-%m-%d").date()
    available_date = datetime.strptime(request.form.get("available_date"),"%Y-%m-%d").date()
    description = request.form.get("description")
    
    # Fetch customer data for pop in user dashboard
    customer = Customer.query.filter_by(customer_id = customer_id).first()
    
    # Fetch all service data for pop up in user dashboard
    service = Services.query.all()
    
    # Create instance of service request by the customer
    service_requested = Service_Request(service_id=service_id,customer_id=customer_id,date_of_request=request_date,date_of_completion=available_date,problem_description=description)
    db.session.add(service_requested)
    
    # Commit changes to the database
    db.session.commit()
    
    # After add service return to user dashboard
    return render_template("user_dashboard.html",customer_name=customer.customer_name,customer_id=customer.customer_id,service=service)
  
  # Add service form rendered
  return render_template("service_request.html",customer_id=customer_id,service=service)


@app.route("/user_history/<int:customer_id>")
def user_history(customer_id):
  '''
    Provide user history and user can edit and close the request.
  '''
  
  # Filter out all service request made by the customer
  user_requests = Service_Request.query.filter_by(customer_id = customer_id).all()
  service_list = []
  
  for user_request in user_requests:
    # Filter out all service cooresponding to particular customer request
    service = Services.query.filter_by(service_id = user_request.service_id).first()
    service_list.append(service)
    
  # Render user history of all the servies requested
  return render_template("user_history.html",service_list=service_list,user_requests=user_requests)


@app.route("/edit_service/<int:service_request_id>",methods=["GET","POST"])
def edit_service(service_request_id):
  '''
    Edit the request made by the customer and commit it to the database.
  '''
  
  # Filter out the service request to be edited
  edit_request = Service_Request.query.filter_by(service_request_id = service_request_id).first()
  
  # Filter out the service information
  service = Services.query.filter_by(service_id = edit_request.service_id).first()
  
  if(request.method == "POST"):
    # Fetch data from edit_request.html and convert date into python date object
    request_date = datetime.strptime(request.form.get("request_date"),"%Y-%m-%d").date()
    available_date = datetime.strptime(request.form.get("available_date"),"%Y-%m-%d").date()
    description = request.form.get("description")
    
    # update the service_request
    edit_request.date_of_request = request_date
    edit_request.date_of_completion = available_date
    edit_request.description = description
    
    # commit changes to the database 
    db.session.commit()
    
    # Fetch customer data to pop up in user_dashboard
    customer = Customer.query.filter_by(customer_id = edit_request.customer_id).first()
    
    # Fetch service data to pop up in user_dashboard
    service = Services.query.all()
    
    # After edit return to user_dashboard
    return render_template("user_dashboard.html",customer_name=customer.customer_name,customer_id=customer.customer_id,service=service)
  
  # Service edit request form rendered
  return render_template("edit_request.html",edit_request=edit_request,service=service)


@app.route("/close_service",methods=["GET","POST"])
def close_service():
  '''
    Customer can close the service.
  '''
  pass
