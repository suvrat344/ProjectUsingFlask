from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Customer(db.Model):
  __tablename__ = "customer"
  customer_id = db.Column(db.Integer,primary_key = True,autoincrement = True)
  user_name = db.Column(db.String,nullable = True)
  customer_name = db.Column(db.String,nullable = True)
  email = db.Column(db.String,nullable = True)
  password = db.Column(db.String,nullable = True)
  
class Professional(db.Model):
  __tablename__ = "professional" 
  professional_id = db.Column(db.Integer,primary_key = True,autoincrement = True)
  user_name = db.Column(db.String,nullable = True)
  professional_name = db.Column(db.String,nullable = True)
  experience = db.Column(db.Integer,nullable = True)
  service_type = db.Column(db.String,nullable = True)
  email = db.Column(db.String,nullable = True)
  password = db.Column(db.String,nullable = True)
  
class Services(db.Model):
  __tablename__ = "services_offered"
  service_id = db.Column(db.Integer,primary_key = True,autoincrement=True)
  service_name = db.Column(db.String,nullable = True)
  description = db.Column(db.String,nullable = True)
  image_url = db.Column(db.String,nullable = True)
  price = db.Column(db.Integer,nullable = True)
  time_required = db.Column(db.Integer,nullable = True)
  
class Service_Request(db.Model):
  __tablename__ = "service_request"
  service_request_id = db.Column(db.Integer,primary_key = True,autoincrement=True)
  service_id = db.Column(db.Integer,db.ForeignKey("services_offered.service_id"))
  customer_id =db.Column(db.Integer,db.ForeignKey("customer.customer_id"),nullable = True)
  professional_id =db.Column(db.Integer,db.ForeignKey("professional.professional_id"),nullable = True)
  date_of_request = db.Column(db.Date,nullable = True)
  date_of_completion = db.Column(db.Date,nullable = True)
  service_status = db.Column(db.String,nullable = True)
  problem_description = db.Column(db.String,nullable=True)
  remarks = db.Column(db.String,nullable = True)
