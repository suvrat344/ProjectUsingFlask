from flask import Flask,render_template,request,redirect,url_for
from flask import current_app as app
from datetime import datetime
from .models import *


@app.route("/")                                                   
def home():
  service = Services.query.all()
  return render_template("home.html")


@app.route("/signup",methods=["GET","POST"])                      
def signup():
  services = Services.query.all()
  if(request.method == "POST"):
    # Fetch common attribute
    role = request.form.get("role")
    email = request.form.get("email")
    name = request.form.get("full_name")
    user_name = request.form.get("uname")
    password = request.form.get("pwd")
    city = request.form.get("city")
    pin_code = request.form.get("pin_code")
    # Check user exist
    new_user = User.query.filter_by(user_name = user_name).first()
    if(new_user is None):
      # Create new user
      new_user = User(
                    user_name = user_name,
                    password = password,
                    role = role
                    )
      db.session.add(new_user)
      db.session.commit()
      # Check role
      if(role == "Customer"):
        address = request.form.get("address")
        customer_info = {
          "customer_name" : name,
          "email" : email,
          "city" : city,
          "pin_code" : pin_code,
          "address" : address,
          "user_id" : new_user.user_id
         }
        add_customer(customer_info)
        return redirect(url_for("login"))
      elif(role == "Professional"):
        experience = request.form.get("experience")
        specialization = request.form.get("specialization")
        print(specialization)
        professional_info = {
          "professional_name" : name,
          "email" : email,
          "city" : city,
          "pin_code" : pin_code,
          "experience" : experience,
          "service_type" : specialization,
          "user_id" : new_user.user_id
        }
        add_professional(professional_info)
        return redirect(url_for("login"))
    else:
      return render_template("signup.html",msg="User already exist")
  else:
    return render_template("signup.html",services = services)
  
  
@app.route("/login",methods=["GET","POST"])                        
def login():
  if(request.method == "POST"):
    # Fetch data
    user_name = request.form.get("uname")
    password = request.form.get("pwd")
    # Check Exist
    user = User.query.filter_by(user_name = user_name).first()
    if(user):
      # Check password
      if(password != user.password):
        return render_template("login.html",msg2="Incorrect Password")
      else:
        # Check role
        if(user.role == "Customer"):
          return redirect(url_for("customer_dashboard",user_id = user.user_id))
        elif(user.role == "Professional"):
          return redirect(url_for("professional_dashboard",user_id = user.user_id))
        else:
          return redirect(url_for("admin_dashboard",user_id = user.user_id))
    else:
      return render_template("login.html",msg1="User name does not exist.")
  else: 
    return render_template("login.html")


#-----------------------------Customer Methods ---------------------------------
def add_customer(customer_info):
  last_customer = Customer.query.order_by(Customer.customer_id.desc()).first()
  if last_customer:
    customer_id = last_customer.customer_id + 1
  else:
    customer_id = 1000
    
  new_customer = Customer(
    customer_id = customer_id,
    customer_name = customer_info["customer_name"],
    email = customer_info["email"],
    city = customer_info["city"],
    pin_code = customer_info["pin_code"],
    address = customer_info["address"],
    user_id = customer_info["user_id"]
    )
  db.session.add(new_customer)
  db.session.commit()
  
@app.route("/customer_dashboard/<int:user_id>")
def customer_dashboard(user_id):
  customer = Customer.query.filter_by(user_id = user_id).first()
  service = Services.query.all()
  return render_template("customer_dashboard.html",
                         customer = customer,
                         service = service
                        )


@app.route("/add_service/<int:user_id>/<int:service_id>",methods=["GET","POST"])
def add_customer_service(user_id,service_id):
  '''
    Add new service requested by the customer.
  '''
  # Filter service
  service = Services.query.get(service_id)
  if(request.method == "POST"):
    # Fetch data
    customer = Customer.query.filter_by(user_id = user_id).first()
    request_date = datetime.strptime(request.form.get("request_date"),"%Y-%m-%d").date()
    available_date = datetime.strptime(request.form.get("available_date"),"%Y-%m-%d").date()
    description = request.form.get("description")
    
    # Create new service request
    service_requested = Service_Request(
      service_id = service_id,
      customer_id = customer.customer_id,
      date_of_request = request_date,
      date_of_completion = available_date,
      problem_description = description
      )
    
    
    
    db.session.add(service_requested)
    db.session.commit()
    
    # Render customer dashboard
    return redirect(url_for("customer_dashboard",
                            user_id = user_id
                           ))
  else:
    return render_template("customer_service_request.html",
                           user_id = user_id,
                           service = service
                          )


@app.route("/customer_history/<int:customer_id>")
def customer_history(customer_id):
  '''
    Provide user history and user can edit and close the request.
  '''
  
  # Filter customer
  customer = Customer.query.get(customer_id)
  # Filter all service requests
  customer_requests = customer.customer_service_requests
  customer_pending_request = []
  customer_completed_request = []
  service_pending_list = []
  service_completed_list = []
  
  for customer_request in customer_requests:
    service = Services.query.get(customer_request.service_id)
    if(customer_request.service_status == "Pending"):
      customer_pending_request.append(customer_request)
      service_pending_list.append(service)
    else:
      customer_completed_request.append(customer_request)
      service_completed_list.append(service)
  return render_template(
                        "customer_history.html",
                        customer_requests = customer_requests,
                        customer_pending_request = customer_pending_request,
                        service_pending_list = service_pending_list,
                        customer_completed_request = customer_completed_request,
                        service_completed_list = service_completed_list
                        )


@app.route("/edit_customer_service/<int:service_request_id>",methods=["GET","POST"])
def edit_customer_service(service_request_id):
  '''
    Edit the request made by the customer and commit it to the database.
  '''
  
  # Filter service request to be edited
  edit_request = Service_Request.query.get(service_request_id)
  service = edit_request.related_service
  
  if(request.method == "POST"):
    # Fetch data
    request_date = datetime.strptime(request.form.get("request_date"),"%Y-%m-%d").date()
    available_date = datetime.strptime(request.form.get("available_date"),"%Y-%m-%d").date()
    description = request.form.get("description")
    
    # update the service_request
    edit_request.date_of_request = request_date
    edit_request.date_of_completion = available_date
    edit_request.description = description
    
    # commit changes to the database 
    db.session.commit()
    
    # Fetch customer data
    customer = edit_request.requesting_customer
    
    # Render customer dashboard
    return redirect(url_for("customer_dashboard",user_id = customer.user_id))
  else:
    return render_template(
                    "customer_edit_request.html",
                    edit_request = edit_request,
                    service = service
                    )


@app.route("/close_service",methods=["GET","POST"])
def close_customer_service():
  '''
    Customer can close the service.
  '''
  pass


#------------------------------ Professional Methods ------------------------------
def add_professional(professional_info):
  last_professional = Professional.query.order_by(Professional.professional_id.desc()).first()
  if last_professional:
    professional_id = last_professional.professional_id + 1
  else:
    professional_id = 10000
    
  new_professional = Professional(
    professional_id = professional_id,
    professional_name = professional_info["professional_name"],
    email = professional_info["email"],
    city = professional_info["city"],
    pin_code = professional_info["pin_code"],
    experience = professional_info["experience"],
    service_type = professional_info["service_type"],
    user_id = professional_info["user_id"]
    )
  db.session.add(new_professional)
  db.session.commit()

  
def professional_notification(professional):  
  # Fetch service detail
  service = Services.query.filter_by(service_name = professional.service_type).first()
  # Fetch service request detail
  service_requests = [request for request in service.service_correspond_request if request.service_status=="Pending"]
  customer_address = []          # List for customer addresss
  service_request_detail = []
  for service_request in service_requests:
    # Fetch customer whose city is same as professional city
    customer = service_request.requesting_customer if service_request.requesting_customer.city == professional.city else None
    pending_request = Professional_Action.query.filter(
                                Professional_Action.service_request_id == service_request.service_request_id,
                                Professional_Action.professional_id == professional.professional_id,
                                Professional_Action.action_type.in_(["Accept","Reject","Pending"])
    ).first()
    
    if(not pending_request and customer):
      customer_address.append(customer)
      service_request_detail.append(service_request)
      professional_option = Professional_Action(
                                              service_request_id = service_request.service_request_id,
                                              professional_id = professional.professional_id,
                                              action_type = "Pending"
                                              )
      db.session.add(professional_option)
      db.session.commit()
    elif(customer and pending_request.action_type not in ["Accept","Reject"]):
      customer_address.append(customer)
      service_request_detail.append(service_request)
  return service_request_detail,customer_address


@app.route("/professional_dashboard/<int:user_id>")
def professional_dashboard(user_id):
  professional = Professional.query.filter_by(user_id = user_id).first()
  service_request_detail,customer_address = professional_notification(professional)
  pending_request = Professional_Action.query.filter_by(
                                          professional_id = professional.professional_id,
                                          action_type = "Pending"
                                          ).all()
  return render_template("professional_dashboard.html",
                         professional = professional,
                         service_request_detail = service_request_detail,
                         pending_request = pending_request,
                         customer_address=customer_address
                         )


@app.route("/professional_request_result/<int:service_request_id>/<int:professional_id>",methods = ["GET","POST"])
def professional_request_result(service_request_id,professional_id):
  if(request.method == "POST"):
    professional = Professional.query.get(professional_id = professional_id)
    service_request = Service_Request.query.get(service_request_id)
    professional_action = Professional_Action.query.filter_by(
                                    professional_id = professional_id,
                                    service_request_id = service_request_id
                                    ).first()
    professional_response = request.form.get("action")
    
    if(professional_response == "Accept" and service_request.service_status not in ["Accept","Close"]):
      service_request.service_status = professional_response
      service_request.professional_id = professional_id
      professional_action.action_type = "Accept"
      db.session.commit()
      
    elif(professional_response == "Reject"):
      professional_action.action_type = "Reject"
      db.session.commit()
    
    return redirect(url_for(
                      "professional_dashboard",
                      user_id = professional.user_id,
                      ))


@app.route("/professional_history/<int:user_id>")
def professional_history(user_id):
  professional = Professional.query.filter_by(user_id = user_id).first()
  # Fetch professional action ("Accept","Reject")
  professional_history = Professional_Action.query.filter(
                          Professional_Action.professional_id == professional.professional_id,Professional_Action.action_type.in_(["Accept","Reject"])
                          ).all()
  service_request_detail = []
  customer_address = []
  
  for history in professional_history:
    service_request = history.related_service_request
    customer = service_request.requesting_customer
    service_request_detail.append(service_request)
    customer_address.append(customer)
  
    
  return render_template(
                      "professional_history.html",
                      professional_history = professional_history,
                      customer_address = customer_address,
                      service_request_detail = service_request_detail
                      )


#----------------------------  Admin Methods ---------------------------------------
@app.route("/admin_dashboard")
def admin_dashboard():
  return render_template("admin_dashboard.html")

@app.route("/customer_detail")
def customer_detail():
  customers = Customer.query.all()
  return render_template("admin_customer_detail.html",customers = customers)

@app.route("/service_detail")
def service_detail():
  services = Services.query.all()
  return render_template("admin_service_detail.html",services = services)

@app.route("/update_service/<int:service_id>",methods = ["GET","POST"])
def update_service(service_id):
  service = Services.query.get(service_id)
  if(request.method == "POST"):
    service_name = request.form.get("service_name")
    service_description = request.form.get("description")
    image_url = request.form.get("url")
    price = request.form.get("price")
    time_required = request.form.get("time_required")
  
    service.service_name = service_name
    service.description = service_description.strip()
    service.image_url = image_url
    service.price = price
    service.time_required = time_required
    
    db.session.commit()
    return redirect(url_for("service_detail"))
  else:  
    return render_template("admin_update_service.html",service = service)

@app.route("/delete_service/<int:service_id>",methods = ["GET","POST"])
def delete_service(service_id):
  service = Services.query.get(service_id)
  db.session.delete(service)
  db.session.commit()
  return redirect(request.referrer)

@app.route("/professional_detail")
def professional_detail():
  professionals = Professional.query.all()
  return render_template("admin_professional_detail.html",professionals = professionals)