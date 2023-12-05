from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from email_notification import send_email
from models import User, Card, Transaction, Product


# Setup
app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/DRSBaza'
db = SQLAlchemy(app)
CORS(app, supports_credentials=True)

adminMailAddress = 'drsadmin@gmail.com'

# Admin
Users = [
    User(
        firstname='admin',
        lastname='drs',
        address='Kralja Petra Prvog 1',
        city='Novi Sad',
        country='Srbija',
        phone='021450810',
        email=adminMailAddress,
        password='123'
    )
]
#Users = db["users"]
Products = db["products"]
Transactions = db["transactions"]


# Logged user
logged_user = None


# Login
@app.route('/Login', methods=['POST'])
def login():
    email = request.json['email']
    password = request.json['password']
    global logged_user

    for user in Users:
        if user.email == email:
            logged_user = user
            break

    app.logger.info(f"\nEmail: {email}\nPassword: {password}")

    response_data = {
        "message": "User successfully registered",
        "email": email,
        "password": password
    }

    return jsonify(response_data), 200


# Register
@app.route('/Register', methods=['POST'])
def register():
    fname = request.json['firstname']
    lname = request.json['lastname']
    address = request.json['address']
    city = request.json['address']
    country = request.json['country']
    phone = request.json['phone']
    email = request.json['email']
    password = request.json['password']

    app.logger.info(
        f"\nName: {fname}\nLast name: {lname}\nAddress:{address}"
        f"\nCity: {city}\nCountry: {country}\nPhone number: {phone}"
        f"\nEmail: {email}\nPassword: {password}")

    # Send mail to admin
    subject = "New user registered"
    body = (f"User details:\nName: {fname}\nLast name: {lname}"
            f"\nAddress: {address}\nCity: {city}\nCountry: {country}"
            f"\nPhone number: {phone}\nEmail: {email}\nPassword: {password}")
    receiver = adminMailAddress

    send_email(subject, body, receiver)

    response_data = {
        "message": "New user successfully registered",
        "email": email,
        "password": password,
        "firstname": fname,
        "lastname": lname,
        "address": address,
        "city": city,
        "country": country,
        "phone": phone
    }

    return jsonify(response_data), 200


# Add new product
@app.route('/AddProduct', methods=['POST'])
def add_product():
    name = request.json['name']
    price = request.json['price']
    currency = request.json.get('currency')
    amount = request.json['amount']
    seller = request.json['seller']

    Products.append(Product(name, seller, price, currency, amount))

    app.logger.info(f"\nProduct name: {name}\nprice: {price}"
                    f"\ncurrency: {currency}\namount {amount}"
                    f"\nseller {seller}")

    response_data = {
        "message": "Product successfully added",
        "name": name,
        "price": price,
        "currency": currency,
        "amount": amount,
        "seller": seller,
    }

    return jsonify(response_data), 200


# Update profile - GET
@app.route('/UpdateProfile', methods=['GET'])
def update_profile():
    global logged_user

    data = {}

    if logged_user is not None:
        data = {
            "firstname": logged_user.firstname,
            "lastname": logged_user.lastname,
            "address": logged_user.address,
            "city": logged_user.city,
            "country": logged_user.country,
            "phone": logged_user.phone,
            "email": logged_user.email,
            "password": logged_user.password
        }

    return jsonify(data)


# Update profile - POST
@app.route('/UpdateProfile', methods=['POST'])
def update_profile():
    fname = request.json['firstname']
    lname = request.json['lastname']
    address = request.json['address']
    city = request.json['address']
    country = request.json['country']
    phone = request.json['phone']
    email = request.json['email']
    password = request.json['password']

    global logged_user

    for user in Users:
        if user.firstame != fname:
            logged_user.firstname = fname

        if user.lastName != lname:
            logged_user.lastname = lname

        if user.address != address:
            logged_user.address = address

        if user.city != city:
            logged_user.city = city

        if user.country != country:
            logged_user.country = country

        if user.phone != phone:
            logged_user.phone = phone

        if user.email != email:
            logged_user.email = email

        if user.password != password:
            logged_user.password = password

    app.logger.info(f"Email: {email}, Password: {password}")
    app.logger.info(
        f"Name: {fname}, Last name: {lname}, Address: {address}, "
        f"City: {city}, Country: {country}, Phone: {phone}")

    response_data = {
        "message": "Profile successfully updated",
        "email": email,
        "password": password,
        "firstname": fname,
        "lastname": lname,
        "address": address,
        "city": city,
        "country": country,
        "phone": phone
    }

    return jsonify(response_data), 200


# Add card to user account
@app.route('/AddCard', methods=['POST'])
def add_card():
    card_num = request.json['cardNum']
    card_date = request.json['cardDate']
    card_cvv = request.json.get('cardCvv')

    app.logger.info(f"\nCard number: {card_num}\nValid until: {card_date}\nCVV: {card_cvv}")

    # TODO connect card to user

    response_data = {
        "message": "Card sucessfully aded",
        "cardNum": card_num,
        "cardDate": card_date,
        "cardCvv": card_cvv,
    }

    return jsonify(response_data), 200


# INDEX - shows all products and logged user info
@app.route('/', methods=['GET'])
def get_all_products():
    data = [
        {
            'name': product.name,
            'price': product.price,
            'currency': product.currency,
            'amount': product.amount,
            'seller': product.seller,
        }
        for product in Products
    ]

    global logged_user
    logged_user_and_products = {}
    if logged_user is not None:
        logged_user_and_products = {
            'email': logged_user.email,
            'products': data
        }
    else:
        logged_user_and_products = {
            'email': '',
            'products': data
        }

    return jsonify(logged_user_and_products)


# Main
if __name__ == "__main__":
    app.run(debug=True)
