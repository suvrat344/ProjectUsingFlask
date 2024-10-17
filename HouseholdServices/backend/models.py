from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Services(db.Model):
  __tablename__ = "services_offered"
  service_id = db.Column(db.Integer,primary_key = True,auto_increment=True)
  service_name = db.Column(db.String,nullable = False)
  description = db.Column(db.String,nullable=False)
  image_url = db.Column(db.String,nullable=False)
  price = db.Column(db.Integer,nullable=False)
  
class Customer(db.Model):
  __tablename__ = "customer"
  customer_id = db.Column(db.Integer,primary_key = True,auto_increment=True)
  user_name = db.Column(db.String,nullable=False)
  customer_name = db.Column(db.String,nullable = False)
  email = db.Column(db.String,nullable=False)
  password = db.Column(db.String,nullable = False)