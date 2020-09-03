from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


#When using flask_restful every Resource has to be a class
#For eg: the resource Student
class Item(Resource):

    parser = reqparse.RequestParser() #Parsing the data which will be sent by client in json format
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field can't be blank") 
    
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every item needs a store id.") 

    @jwt_required() # If we use this decorator it means user will have to authenticate before making a get call
    def get(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json() #.json() is a method in item.py file in models folder
        return {'message':'Item not found'}

    
    
    def post(self,name): 
        #Making sure that items are unique in our db
        if  ItemModel.find_by_name(name):
            return {'message':f"Item with name {name} already exists"},400
        
        data = Item.parser.parse_args()
        item = ItemModel(name ,data['price'],data['store_id'])
        
        try:
            item.save_to_db()
        except:
            return {"message":"An error occurred while inserting the item"},500 #Internal server error
        return item.json() ,201

    
    def delete(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        
        return {'message':'Item has been deleted'}

    def put(self,name):
       
        data = Item.parser.parse_args() #This makes sure that even if client send more fields only the price will be passed into the data variable
        
        item = ItemModel.find_by_name(name)
        
        if item is None: 
            item = ItemModel(name,data['price'],data['store_id'])
        else:
            item.price = data['price']

        item.save_to_db()    
        return item.json()

    
class ItemList(Resource):
    def get(self):
        return {'items':[item.json() for item in ItemModel.query.all()]}
        