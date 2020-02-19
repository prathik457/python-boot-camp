from flask_restful import Resource
from src.models.item_model import ItemModel
from flask import request
import sqlalchemy

class Item(Resource):

    def get(self, name):
        try:
            item = ItemModel.get_item_by_name(name)
            return item.json(), 200
        except Exception:
            return {'message': 'Item not found'}, 404

    def post(self, name):
        try:
            payload = request.get_json()
            item = ItemModel(name, payload['description'], payload['price'])
            item.save()
            return item.json(), 201
        except sqlalchemy.exc.IntegrityError:
            return {'message': 'Item already exists'}, 400
        except Exception:
            return {'message': 'Error encountered while creating item'}, 400

    def put(self, name):
        pass

    def delete(self, name):
        pass