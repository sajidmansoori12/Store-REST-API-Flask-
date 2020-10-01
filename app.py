import os

from flask import Flask 
from flask_restful import Api
from flask_jwt import JWT #using for java web token 


from resources.user import UserRegister 
from security import authenticate,identity #The functions that we defined in security.py
from resources.item import Item,ItemList
from resources.store import Store,StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #This turns off the flask's modification tracking as SQLAlchemy has it's own tracker which is better than flask's.
app.secret_key = 'sajid' #This secret key will be used to create jwt 
api = Api(app) 


jwt = JWT(app,authenticate,identity) #This will create an endpoint whose url will be '/auth'
""" Note that authenticate function will be used whenever /auth endpoint is called and 
identity function will be called whenever an endpoint which uses an auth token is called."""



api.add_resource(Item,'/item/<string:name>')
api.add_resource(ItemList,'/items')
api.add_resource(UserRegister,'/register')
api.add_resource(Store,'/store/<string:name>')
api.add_resource(StoreList,'/stores')
if __name__=='__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000,debug=True)#debug=False
