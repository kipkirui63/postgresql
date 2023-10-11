# app.py
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://sang_user:s4dkioRiO8mCiCXQsNGOuZmm9qQUko2y@dpg-ckjebh4l4vmc73bb2dsg-a.ohio-postgres.render.com/sang'


db = SQLAlchemy(app)


def create_app(): 
    CORS(app)

    CORS(app, origins="*")

    # db.init_app(app)

    
    # added routes
    from app import routes

    return app
