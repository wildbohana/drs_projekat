from flask import Flask, session, jsonify, make_response
from flask_restful import Api, reqparse, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flaskext.mysql import MySQL
from flask_cors import CORS
import hashlib

from multiprocessing import Queue

app = Flask(__name__)

# Connection for dockerized MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:123@localhost:3333/drs_sema'
app.config['SQLALCHEMY_POOL_SIZE'] = 5
app.config['SQLALCHEMY_MAX_OVERFLOW'] = 2
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '123'
app.config['MYSQL_DATABASE_DB'] = 'drs_sema'
app.config['MYSQL_DATABASE_HOST'] = 'localhost:3333'

api = Api(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)
mysql = MySQL(app)
CORS(app, supports_credentials=True)

# Dict(Key, value) = token, email
activeTokens = {}

# Email queue
emailQueue = Queue()


# Hash for token
def create_hash(text, end="_anavolimilovana"):
    hash_text = text + end
    return hashlib.sha256(hash_text.encode("utf8")).hexdigest()
