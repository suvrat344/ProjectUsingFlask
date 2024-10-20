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
    # Fetch data from login form
    user_name = request.form.get("uname")
    password = request.form.get("pwd")
    # Check user exist or not
    user = User.query.filter_by(user_name = user_name).first()
    service = Services.query.all()
    if(user):
      if(password != user.password):
        return render_template("login.html",msg2="Incorrect Password")
      else:
        if(user.role == "Customer"):
          customer = Customer.query.filter_by(user_id = user.user_id).first()
          return render_template("customer_dashboard.html",customer_name = customer.customer_name,customer_id=customer.customer_id,service=service)
        else:
          professional = Professional.query.filter_by(user_id = user.user_id).first()
          return render_template("professional_dashboard.html",professional_name = professional.professional_name,professional_id=professional.professional_id)
    else:
      return render_template("login.html",msg1="User name does not exist.")
  return render_template("login.html")


@app.route("/signup",methods=["GET","POST"])                      
def signup():
  if(request.method == "POST"):
    # Fetch out common attribute of customer and professional
    role = request.form.get("role")
    email = request.form.get("email")
    name = request.form.get("full_name")
    user_name = request.form.get("uname")
    password = request.form.get("pwd")
    city = request.form.get("city")
    pin_code = request.form.get("pin_code")
    
    # Check user already exist or not
    new_user = User.query.filter_by(user_name = user_name).first()
    
    if(new_user is None):
      # If user not exist then enter user data
      new_user = User(user_name=user_name,password=password,role=role)
      db.session.add(new_user)
      db.session.commit()
      
      if(role == "Customer"):
        address = request.form.get("address")
        new_customer = Customer(customer_name=name,email=email,city=city,pin_code=pin_code,address=address,user_id=new_user.user_id)
        db.session.add(new_customer)
        db.session.commit()
        return render_template("login.html")
      elif(role=="Professional"):
        experience = request.form.get("experience")
        specialization = request.form.get("specialization")
        new_professional = Professional(professional_name=name,email=email,city=city,pin_code=pin_code,experience=experience,service_type=specialization,user_id=new_user.user_id)
        db.session.add(new_professional)
        db.session.commit()
        return render_template("login.html")
    else:
      # If user already exist
      return render_template("signup.html",msg="User already exist")
  return render_template("signup.html")

#-----------------------------Customer Methods ---------------------------------

@app.route("/add_service/<int:customer_id>/<int:service_id>",methods=["GET","POST"])
def add_service(customer_id,service_id):
  '''
    Add new service requested by the customer.
  '''
  
  # Filter out service requested by the customer
  service = Services.query.filter_by(service_id = service_id).first()
  if(request.method == "POST"):
    # Fetch data from customer_service_request.html and convert date into python date object
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
    return render_template("customer_dashboard.html",customer_name=customer.customer_name,customer_id=customer.customer_id,service=service)
  
  # Add service form rendered
  return render_template("customer_service_request.html",customer_id=customer_id,service=service)


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
  return render_template("customer_history.html",service_list=service_list,user_requests=user_requests)


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
    return render_template("customer_dashboard.html",customer_name=customer.customer_name,customer_id=customer.customer_id,service=service)
  
  # Service edit request form rendered
  return render_template("customer_edit_request.html",edit_request=edit_request,service=service)


@app.route("/close_service",methods=["GET","POST"])
def close_service():
  '''
    Customer can close the service.
  '''
  pass



#------------------------------ Professional Methods ------------------------------



#----------------------------  Admin Methods ---------------------------------------