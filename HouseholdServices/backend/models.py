from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import PrimaryKeyConstraint,CheckConstraint

db = SQLAlchemy()
    
class User(db.Model):
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String, nullable = False)
    password = db.Column(db.String, nullable = False)
    role = db.Column(db.String, nullable = False)
    
    __table_args__ = (
        CheckConstraint(
            "role in ('Admin','Customer','Professional')",
            name = "check_role"
        ),
    )
    
    # One-to-One relationship with Customer
    customer = db.relationship("Customer", uselist = False, backref = "user")
    
    # One-to-One relationship with Professional
    professional = db.relationship("Professional", uselist = False, backref = "user")

class Customer(db.Model):
    __tablename__ = "customer"
    customer_id = db.Column(db.Integer,primary_key=True)
    customer_name = db.Column(db.String, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id",ondelete = "CASCADE"),nullable = False)
    email = db.Column(db.String, nullable = False)
    city = db.Column(db.String, nullable = False)
    image_url = db.Column(db.String, nullable = False)
    pin_code = db.Column(db.Integer, nullable = False)
    address = db.Column(db.String, nullable = False)
    customer_service_requests = db.relationship("Service_Request", backref = "requesting_customer")

class Professional(db.Model):
    __tablename__ = "professional"
    professional_id = db.Column(db.Integer,primary_key=True)
    professional_name = db.Column(db.String, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id",ondelete = "CASCADE"),nullable = False)
    image_url = db.Column(db.String, nullable = False)
    experience = db.Column(db.Integer, nullable = False)
    service_type = db.Column(db.String, nullable = False)
    email = db.Column(db.String, nullable = False)
    city = db.Column(db.String, nullable = False)
    pin_code = db.Column(db.Integer, nullable = False)
    professional_service_requests = db.relationship("Service_Request", backref="assigned_professional")
    

class Services(db.Model):
    __tablename__ = "services_offered"
    service_id = db.Column(db.Integer,primary_key=True,default = 100,autoincrement = True)
    service_name = db.Column(db.String, nullable = False)
    description = db.Column(db.String, nullable = False)
    image_url = db.Column(db.String, nullable = False)
    price = db.Column(db.Integer, nullable = False)
    time_required = db.Column(db.Integer, nullable = False)
    service_correspond_request = db.relationship("Service_Request", backref = "related_service")
  

class Service_Request(db.Model):
    __tablename__ = "service_request"
    service_request_id = db.Column(db.Integer,primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey("services_offered.service_id",ondelete = "CASCADE"))
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.customer_id",ondelete = "CASCADE"), nullable = False)
    professional_id = db.Column(db.Integer, db.ForeignKey("professional.professional_id",ondelete = "CASCADE"), nullable = False)
    date_of_request = db.Column(db.Date, nullable = False)
    date_of_completion = db.Column(db.Date, nullable = True)
    service_status = db.Column(db.String, default="Pending", nullable = False)
    problem_description = db.Column(db.String, nullable = True)
    professional_rating = db.Column(db.Integer, nullable = True)
    remarks = db.Column(db.String, nullable = True)
    actions = db.relationship("Professional_Action", backref = "related_service_request")
   
    __table_args__ = (
        CheckConstraint(
            "service_status in ('Pending','Accept','Close')",
            name = "check_service_status"
        ),
    )

class Professional_Action(db.Model):
    __tablename__ = "professional_action"
    service_request_id = db.Column(db.Integer, db.ForeignKey("service_request.service_request_id",ondelete = "CASCADE"))
    professional_id = db.Column(db.Integer, db.ForeignKey("professional.professional_id",ondelete = "CASCADE"))
    action_type = db.Column(db.String,nullable = False)
    
    __table_args__ = (
        PrimaryKeyConstraint("service_request_id", "professional_id"),
    )