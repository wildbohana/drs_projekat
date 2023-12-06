from Models.User import User
from Configuration.config import api, db, reqparse, Resource, jsonify, make_response

#region LOGIN
userLoginArgs = reqparse.RequestParser()
userLoginArgs.add_argument("email", type=str, help="Email is required", required=True)
userLoginArgs.add_argument("password", type=str, help="Password is required", required=True)


# User login - POST
class Login(Resource):
    def post(self):
        args = userLoginArgs.parse_args()
        global loggedUser

        try:
            temp = db.session.execute(db.select(User).filter_by(email=args["email"])).one_or_none()
            if not temp:
                return "User doesnt exist!", 400

            if temp.password != args['password']:
                return "Invalid password", 400

            if args["email"] == loggedUser:
                return "User already logged in", 400

            loggedUser = args["email"]

            return make_response(jsonify({"token": loggedUser}), 200)
        except Exception as e:
            return "Error: " + str(e), 500


api.add_resource(Login, "/login")
#endregion


#region LOGOUT
class Logout(Resource):
    def post(self, token):
        global loggedUser
        try:
            loggedUser = None
            return "OK", 200
        except Exception as e:
            return "Error: " + str(e), 500


api.add_resource(Logout, "/logout/<string:token>")
#endregion


#region REGISTER
userRegistrationArgs = reqparse.RequestParser()
userRegistrationArgs.add_argument("firstName", type=str, help="First name is required", required=True)
userRegistrationArgs.add_argument("lastName", type=str, help="Last name is required", required=True)
userRegistrationArgs.add_argument("email", type=str, help="E mail is required", required=True)
userRegistrationArgs.add_argument("address", type=str, help="Address is required", required=True)
userRegistrationArgs.add_argument("city", type=str, help="City is required", required=True)
userRegistrationArgs.add_argument("phoneNumber", type=str, help="Phone number is required", required=True)
userRegistrationArgs.add_argument("password", type=str, help="Password is required", required=True)


class Register(Resource):
    def post(self):
        try:
            args = userRegistrationArgs.parse_args()
            temp = db.session.execute(db.select(User).filter_by(email=args["email"])).one_or_none()
            if temp:
                return "Email is taken!", 400

            password = args["password"]
            user = User(firstName=args['firstName'], lastName=args['lastName'],
                        email=args['email'], address=args['address'], city=args['city'],
                        phoneNumber=args['phoneNumber'], password=password, verified=False)
            db.session.add(user)
            db.session.commit()
            return "New user has been created!", 200
        except Exception as e:
            return "Error: " + str(e), 500


api.add_resource(Register, "/register")
#endregion
