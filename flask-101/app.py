from flask import Flask
from flask_restful import Resource, Api
from src.api.item import Item
from src.models import db, create_db_tables

def create_app():
    app = Flask(__name__)
    api = Api(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
    db.init_app(app)
    return app, api

app, api = create_app()

@app.before_first_request
def setup_tables():
    create_db_tables()

class Hello(Resource):
    def get(self):
        return 'Hello World'

api.add_resource(Hello, '/') # this translates to http://<hostname>:<port>/
api.add_resource(Item, '/item/<string:name>')

if(__name__ == '__main__'):
    app.run(port=5000, host='0.0.0.0', debug=True)