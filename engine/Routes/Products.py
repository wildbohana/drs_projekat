from Models.Product import Product, ProductSchema
from Configuration.config import api, db, reqparse, Resource, activeTokens, create_hash, jsonify, make_response


addingProductArgs = reqparse.RequestParser()
addingProductArgs.add_argument("name", type=str, help="Product name is required", required=True)
addingProductArgs.add_argument("price", type=float, help="Product price is required", required=True)
addingProductArgs.add_argument("currency", type=str, help="Currency is required", required=True)
addingProductArgs.add_argument("amount", type=float, help="Amount is required", required=True)


class AddProduct(Resource):
    def post(self):
        try:
            args = addingProductArgs.parse_args()
            temp = db.session.execute(db.select(Product).filter_by(name=args["name"])).one_or_none()
            if temp is not None:
                return "Product already exists!", 400

            product = Product(name=args['name'], price=args['price'],
                              currency=args['currency'], amount=args['amount'])
            db.session.add(product)
            db.session.commit()
            return "New product has been created!", 200
        except Exception as e:
            return "Error: " + str(e), 500


api.add_resource(AddProduct, "/addProduct")


class GetProduct(Resource):
    def get(self, id):
        try:
            temp = db.session.execute(db.select(Product).filter_by(id=id)).one_or_none()
            if temp is None:
                return "Product doesn't exist!", 400

            product_schema = ProductSchema()
            result = product_schema.dump(temp[0])
            return make_response(jsonify(result), 200)
        except Exception as e:
            return "Error: " + str(e), 500


api.add_resource(GetProduct, "/getProduct/<int:id>")


class GetAllProducts(Resource):
    def get(self):
        try:
            products = db.session.execute(db.select(Product)).all()
            if products is None:
                return "Products don't exist!", 400

            retval = []
            for prod in products:
                product_schema = ProductSchema()
                temp = product_schema.dump(prod[0])
                print(temp)
                retval.append(temp)

            return make_response(jsonify(retval), 200)
        except Exception as e:
            return "Error: " + str(e), 500


api.add_resource(GetAllProducts, "/getAllProducts")


changeAmountArgs = reqparse.RequestParser()
changeAmountArgs.add_argument("amount", type=float, help="Amount is required", required=True)


class ChangeAmount(Resource):
    def patch(self, id):
        try:
            args = changeAmountArgs.parse_args()
            product = db.session.execute(db.select(Product).filter_by(id=id)).one_or_none()
            if product is None:
                return "Product doesn't exist!", 400

            product[0].amount = args['amount']
            db.session.commit()

            return "Product amount has been updated!", 200
        except Exception as e:
            return "Error: " + str(e), 500


api.add_resource(ChangeAmount, "/changeAmount/<int:id>")
