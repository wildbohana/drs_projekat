from Configuration.config import reqparse, api, db, jsonify, Resource, loggedUser, make_response
from Models.User import User, UserSchema

userUpdateArgs = reqparse.RequestParser()
userUpdateArgs.add_argument("firstName", type=str)
userUpdateArgs.add_argument("lastName", type=str)
userUpdateArgs.add_argument("email", type=str)
userUpdateArgs.add_argument("address", type=str)
userUpdateArgs.add_argument("city", type=str)
userUpdateArgs.add_argument("phoneNumber", type=str)
userUpdateArgs.add_argument("password", type=str)


# User profile GET i PATCH (promena)
class UserProfile(Resource):
    def get(self, token):
        global loggedUser

        try:
            if token != loggedUser:
                return "Please login to continue.", 400

            user = db.session.execute(db.select(User).filter_by(email=loggedUser)).one_or_none()['User']
            user_schema = UserSchema()
            result = user_schema.dump(user)
            result.pop('password')
            return make_response(jsonify(result), 200)
        except Exception as e:
            return "Error: " + str(e), 500

    def patch(self, token):
        args = userUpdateArgs.parse_args()
        global loggedUser

        try:
            if token != loggedUser:
                return "Please login to continue.", 400

            account = db.session.execute(db.select(User).filter_by(email=loggedUser)).one_or_none()['User']
            if not account:
                return "User with this email doesn't exist", 404

            if args['firstName']:
                account.firstName = args['firstName']
            if args['lastName']:
                account.lastName = args['lastName']
            if args['email']:
                account.email = args['email']
            if args['address']:
                account.address = args['address']
            if args['city']:
                account.city = args['city']
            if args['phoneNumber']:
                account.phoneNumber = args['phoneNumber']
            if args['password']:
                account.password = args['password']

            db.session.commit()
            user_schema = UserSchema()
            result = user_schema.dump(account)
            loggedUser = account.email
            return make_response(jsonify(result), 200)
        except Exception as e:
            return "Error: " + str(e), 500


api.add_resource(UserProfile, "/userProfile/<string:token>")
