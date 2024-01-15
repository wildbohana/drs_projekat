from Configuration.config import reqparse, api, db, jsonify, Resource, activeTokens, make_response, create_hash
from Models.User import User, UserSchema


userUpdateArgs = reqparse.RequestParser()
userUpdateArgs.add_argument("firstName", type=str)
userUpdateArgs.add_argument("lastName", type=str)
userUpdateArgs.add_argument("email", type=str)
userUpdateArgs.add_argument("address", type=str)
userUpdateArgs.add_argument("city", type=str)
userUpdateArgs.add_argument("state", type=str)
userUpdateArgs.add_argument("phoneNumber", type=str)
userUpdateArgs.add_argument("password", type=str)


# GET i PATCH
class UserProfile(Resource):
    def get(self, token):
        try:
            if token not in activeTokens.keys():
                return "Please login to continue.", 400

            user = db.session.execute(db.select(User).filter_by(email=activeTokens[token])).one_or_none()
            user_schema = UserSchema()
            result = user_schema.dump(user[0])
            result.pop('password')
            return make_response(jsonify(result), 200)
        except Exception as e:
            return "Error: " + str(e), 500

    def patch(self, token):
        args = userUpdateArgs.parse_args()
        try:
            if token not in activeTokens.keys():
                return "Please login to continue.", 400

            account = db.session.execute(db.select(User).filter_by(email=activeTokens[token])).one_or_none()
            if account is None:
                return "User with this email doesn't exist", 404

            if args['firstName']:
                account[0].firstName = args['firstName']
            if args['lastName']:
                account[0].lastName = args['lastName']
            if args['email']:
                account[0].email = args['email']
            if args['address']:
                account[0].address = args['address']
            if args['city']:
                account[0].city = args['city']
            if args['state']:
                account[0].city = args['state']
            if args['phoneNumber']:
                account[0].phoneNumber = args['phoneNumber']
            if args['password']:
                account[0].password = create_hash(args['password'])

            db.session.commit()
            activeTokens[token] = account[0].email

            user_schema = UserSchema()
            result = user_schema.dump(account[0])
            return make_response(jsonify(result), 200)
        except Exception as e:
            return "Error: " + str(e), 500


api.add_resource(UserProfile, "/userProfile/<string:token>")
