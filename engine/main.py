from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy


# Setup
app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/DRSBaza'
db = SQLAlchemy(app)


# Home
@app.route("/")
def home():
    return "Home"


# Test method
@app.route("/members")
def members():
    return {"members": ["Member1", "Member2", "Member3"]}


# Initialize server
if __name__ == "__main__":
    app.run(debug=True, port=5000)


"""
# Vrv izaziva ciklični import
from models.User import User
from models.Card import Card
from models.Product import Product
from models.Transaction import Transaction
"""
