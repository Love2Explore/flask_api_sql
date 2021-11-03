
from flask_restful import Resource,  reqparse
from flask_jwt import  jwt_required
import sqlite3
from models.items import ItemModel

class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price',
                            type=float,
                            required=True,
                            help="This should be provided!")   

    @jwt_required()
    def get(self , name):
        item= ItemModel.find_by_name(name)
        if item:
            print(item)
            return item[0].json()
        else:
            return {"message":"No record Found"} , 404

        # item = next(filter(lambda x: x['name'] == name , items), None)
        # return {'item' :item } , 200 if item else 404
    

    @jwt_required()
    def post(self , name):
        result = ItemModel.find_by_name(name)
        # if next(filter(lambda x: x['name'] == name , items), None):
        #     return {'message':'An item with name {} already exist.'.format(name)} , 400
        if result:
            return {'message':'An item with name {} already exist.'.format(name)} , 400
        # try:
        data = Item.parser.parse_args()
        item = ItemModel(name,data['price']) 
        item.insert()
        # except:
            #  return {"message":"An exception has occur while insurting"}, 500
        return item.json(), 201
        # data = Item.parser.parse_args()
        # item = {'name' : name , 'price' : data['price'] }
        # items.append(item)
        # return item ,201

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name,data['price'])
        # item = next(filter(lambda x: x['name'] == name , items), None)
        if item is None:
            try:
                updated_item.insert()
            except:
                return {"message":"An exception has occur while insurting"}, 500 
        else:
            try:
                updated_item.update()
            except:
                return {"message":"An exception has occur while insurting"}, 500 
        return updated_item.json()

    def delete(self, name):
        result = ItemModel.find_by_name(name)
        if result:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            query = "DELETE FROM items WHERE name = ?"
            cursor.execute(query,(name,))
            connection.commit()
            connection.close()
            return {"message":"Record Deleted Successfully!"} ,201
        


    
class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({"id":row[0],"name":row[1],"price":row[2]})
        connection.close()
        return {"items":items}