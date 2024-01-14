from Models.User import User
from Configuration.config import api, db, reqparse, Resource, jsonify, make_response, activeTokens, create_hash
from Configuration import emails
from datetime import datetime
from flask import request


userRegistrationArgs = reqparse.RequestParser()
userRegistrationArgs.add_argument("firstName", type=str, help="First name is required", required=True)
userRegistrationArgs.add_argument("lastName", type=str, help="Last name is required", required=True)
userRegistrationArgs.add_argument("email", type=str, help="E mail is required", required=True)
userRegistrationArgs.add_argument("password", type=str, help="Password is required", required=True)
userRegistrationArgs.add_argument("address", type=str, help="Address is required", required=True)
userRegistrationArgs.add_argument("city", type=str, help="City is required", required=True)
userRegistrationArgs.add_argument("state", type=str, help="State is required", required=True)
userRegistrationArgs.add_argument("phoneNumber", type=str, help="Phone number is required", required=True)


class Register(Resource):
    def post(self):
        try:
            args = userRegistrationArgs.parse_args()
            temp = db.session.execute(db.select(User).filter_by(email=args["email"])).one_or_none()
            if temp is not None:
                return "Email is taken!", 400

            password = create_hash(args["password"])
            user = User(firstName=args['firstName'], lastName=args['lastName'],
                        address=args['address'], city=args['city'],
                        state=args['state'], phoneNumber=args['phoneNumber'],
                        email=args['email'], password=password, verified=False)

            db.session.add(user)
            db.session.commit()

            # Notify admin about new registration
            subject = "New user registered"
            body = (f"User data:\nFirst name: {args['firstName']}\n"
                    f"Last name: {args['lastName']}\nAddress: {args['address']}\n"
                    f"City: {args['city']}\nState: {args['state']}\n"
                    f"Phone number: {args['phoneNumber']}\nEmail: {args['email']}")
            emails.sendEmail(subject, body)

            return "New user has been created!", 200
        except Exception as e:
            return "Error: " + str(e), 500


api.add_resource(Register, "/register")


userLoginArgs = reqparse.RequestParser()
userLoginArgs.add_argument("email", type=str, help="Email is required", required=True)
userLoginArgs.add_argument("password", type=str, help="Password is required", required=True)


# User login - POST
class Login(Resource):
    def post(self):
        args = userLoginArgs.parse_args()
        try:
            temp = db.session.execute(db.select(User).filter_by(email=args["email"])).one_or_none()
            if temp is None:
                return "User doesnt exist!", 400

            password = create_hash(args['password'])
            if temp[0].password != password:
                return "Invalid password", 400

            if args["email"] in activeTokens.values():
                for key in activeTokens:
                    if activeTokens[key] == args["email"]:
                        return make_response(jsonify({"token": key}), 200)
                return "User already logged in", 400

            token = create_hash(args['email'], str(datetime.now().timestamp()))
            activeTokens[token] = args['email']

            return make_response(jsonify({"token": token}), 200)
        except Exception as e:
            return "Error:" + str(e), 500


api.add_resource(Login, "/login")


class Logout(Resource):
    def post(self, token):
        try:
            activeTokens.pop(token)
            return "OK", 200
        except Exception as e:
            return "Error: " + str(e), 500


api.add_resource(Logout, "/logout/<string:token>")
