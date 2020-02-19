from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_db_tables():
    db.create_all()