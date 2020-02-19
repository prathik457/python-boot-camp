**

## REST with Flask

**
- Go to a the workspace folder where you want to create the project
- pip --version
	- check environment variables
	- sudo apt-get install python-pip (linux)
	- curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py (windows)
		- python get-pip.py
- pip install virtualenv
- Explain virtualenv
- virtualenv <environment_name>
- source <environment_name>/bin/activate (linux)
- <environment_name>\Scripts\activate (Windows)
- pip install Flask-RESTful
- pip freeze > requirements.txt
- open requirements.txt to show the contents
- code . to open VS Code
- create a folder src
- create a file app.py  

```python
from flask import Flask

app = Flask(__name__)

@app.route('/') # this translates to http://<hostname>:<port>/
def  hello():
	return  'Hello World'

if(__name__ == '__main__'):
	app.run(port=5000, host='0.0.0.0', debug=True)
```
- Explain the code
	- __name __ explaination
	- imports explaination
- Explain why use FlaskRestful
```python
from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class  Hello(Resource):
	def  get(self):
		return  'Hello World'  

# this translates to http://<hostname>:<port>/
api.add_resource(Hello, '/')

if(__name__ == '__main__'):
	app.run(port=5000, host='0.0.0.0', debug=True)
```
- Create api folder
	- create item.py
- Create models folder
	- create item_model.py

```python
items = [
	{
		"name": "Colgate",
		"description": "Popular tooth paste",
		"price": 80
	},
	{
		"name": "Monaco",
		"description": "Sweet and salt biscuits",
		"price": 20
	}
]
```
```python
from flask_restful import Resource
from src.models.item_model import items
from flask import request 

class  Item(Resource):
	def  get(self, name):
		for item in items:
			if item['name'] == name:
				return item, 200
		return {'message': 'Item not found!'}, 404

	def  post(self, name):
		for item in items:
			if item['name'] == name:
				return  'Item already exists'
		payload = request.get_json()
		item = {'name': name, 'description': payload['description'], 'price': payload['price']}
		items.append(item)
		return item, 201

	def  put(self, name):
		pass
		
	def  delete(self, name):
		pass
```
```python
from flask import Flask
from flask_restful import Resource, Api
from src.api.item import Item

app = Flask(__name__)
api = Api(app)

class  Hello(Resource):
	def  get(self):
		return  'Hello World'  

# this translates to http://<hostname>:<port>/
api.add_resource(Hello, '/')
api.add_resource(Item, '/item/<string:name>')

if(__name__ == '__main__'):
	app.run(port=5000, host='0.0.0.0', debug=True)
```
- Open Postman to check the code

- Now lets connect to a DB
	- pip install Flask-SQLAlchemy
- Add code to instantiate db connection in app.py
```python
from flask import Flask
from flask_restful import Resource, Api
from src.api.item import Item
from src.models import db, create_db_tables  

def  create_app():
	app = Flask(__name__)
	api = Api(app)
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
	db.init_app(app)
	return app, api

app, api = create_app()  

@app.before_first_request
def  setup_tables():
	create_db_tables()

class  Hello(Resource):
	def  get(self):
		return  'Hello World'

api.add_resource(Hello, '/') # this translates to http://<hostname>:<port>/
api.add_resource(Item, '/item/<string:name>')

if(__name__ == '__main__'):
	app.run(port=5000, host='0.0.0.0', debug=True)
```
- Create a file called __init __.py in models
```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def  create_db_tables():
	db.create_all()
```

- Modify item_model.py
```python
from src.models import db

class  ItemModel(db.Model):
	__tablename__ = 'items'
	_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(150), nullable=False)
	description = db.Column(db.String(300))
	price = db.Column(db.Float(precision=2), nullable=False)

def  __init__(self, name, description, price):
	self.name = name
	self.description = description
	self.price = price

def  save(self):
	db.session.add(self)
	db.session.commit()

def  update(self):
	db.session.commit()

def  delete(self):
	db.session.delete(self)
	db.session.commit()

@classmethod
def  get_items(cls):
	return  cls.query.all()

@classmethod
def  get_item_by_name(cls, name):
	item = cls.query.filter_by(name=name).first()
	return item

def  json(self):
	return {'name': self.name, 'description': self.description, 'price': self.price}
``` 
- Update item.py
```python
from flask_restful import Resource
from src.models.item_model import ItemModel
from flask import request
import sqlalchemy

class  Item(Resource):
	def  get(self, name):
		try:
			item = ItemModel.get_item_by_name(name)
			return item.json(), 200
		except  Exception:
			return {'message': 'Item not found'}, 404

	def  post(self, name):
		try:
			payload = request.get_json()
			item = ItemModel(name, payload['description'], payload['price'])
			item.save()
			return item.json(), 201
		except sqlalchemy.exc.IntegrityError:
			return {'message': 'Item already exists'}, 400
		except  Exception:
			return {'message': 'Error encountered while creating item'}, 400

	def  put(self, name):
		pass

	def  delete(self, name):
		pass
```

