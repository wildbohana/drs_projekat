from Models.Product import Product, ProductSchema
from Configuration.config import api, db, reqparse, Resource, activeTokens, create_hash, jsonify, make_response

#region ADD NEW PRODUCT
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
            if temp:
                return "Product already exists!", 400

            product = Product(name=args['name'], price=args['price'],
                              currency=args['currency'], amount=args['amount'])
            db.session.add(product)
            db.session.commit()
            return "New product has been created!", 200
        except Exception as e:
            return "Error: " + str(e), 500


api.add_resource(AddProduct, "/addProduct")
#endregion


#region GET PRODUCT
getProductArgs = reqparse.RequestParser()
getProductArgs.add_argument("id", type=int, help="Product ID is required", required=True)


class GetProduct(Resource):
    def get(self, id):
        try:
            temp = db.session.execute(db.select(Product).filter_by(id=id)).one_or_none()[0]
            if not temp:
                return "Product doesn't exist!", 400
            product_schema = ProductSchema()
            result = product_schema.dump(temp)
            #result.pop('id')
            return make_response(jsonify(result), 200)
        except Exception as e:
            return "Error: " + str(e), 500


api.add_resource(GetProduct, "/getProduct/<int:id>")
#endregion


#TODO patch (to change amount)
#TODO getAllProducts
