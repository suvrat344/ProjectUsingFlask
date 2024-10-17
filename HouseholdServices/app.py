from flask import Flask
from backend.models import *

app = None                                              

def init_app():
  householdService_app = Flask(__name__)                            
  householdService_app.dubug = True
  householdService_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///householdService.sqlite3"
  householdService_app.app_context().push()                         
  db.init_app(householdService_app)
  print("Household Services application started......")
  return householdService_app
  
app = init_app()
from backend.controllers import *

if(__name__ == "__main__"):
  app.run()