"""
author: Rahul Bera <rbasu611@gmail.com>

Main API file

"""

from flask import Flask, jsonify, request, Response
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt
import json

app = Flask(__name__)
api = Api(app)

# Database Settings
try:
    conn = MongoClient("mongodb://localhost:27017")
    db = conn.amazon_price_tracker
    productCollection = db.products
    usersCollection = db.users
    print("db connected")
except:
    print("error connecting to db")


class CreateUser(Resource):
    def post(self):

        """
        Create a user in a database
        
        """
        postedData = request.get_json()
        email = postedData["email"]
        userName = postedData["username"]
        password = postedData["password"]

        checkedEmail = usersCollection.find_one({"email": email})

        if checkedEmail is None:
            hashedPassword = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(8))

            userDocument = {
                "email": email,
                "password": hashedPassword,
                "username": userName,
            }

            usersCollection.insert_one(userDocument)

            try:
                js = json.dumps(
                    {"message": "User succesfully created", "success": True}
                )
                response = Response(js, status=201, mimetype="application/json")
            except:
                js = json.dumps({"message": "Cannot create a user", "success": False})
                response = Response(js, status=500, mimetype="application/json")

            return response
        else:
            js = json.dumps({"message": "Email already taken", "success": False})

            response = Response(js, status=400, mimetype="application/json")
            return response



class GetUserForLogin(Resource):
    def get(self):
        """
        Check for a user in database
        
        """

        postedData = request.get_json()
        email = postedData["email"]
        password = postedData["password"]

        dbEmail = usersCollection.find_one({"email": email})

        if dbEmail is None:
            js = json.dumps(
                {"message": "Incorrect Email or Password", "success": False}
            )

            reponse = Response(js, status=404, mimetype="application/json")
            return reponse
        else:
            if (
                bcrypt.hashpw(password.encode("utf-8"), dbEmail["password"])
                == dbEmail["password"]
            ):
                js = json.dumps({"message": "successfully logged in", "sucess": True})

                response = Response(js, status=200, mimetype="application/json")
                return response

            else:
                js = json.dumps(
                    {"message": "Incorrect email or password", "sucess ": False}
                )

                response = Response(js, status=404, mimetype="application/json")
                return response


class GetUserName(Resource):
    def get(self):
        """
            API endpoint to get a single user
        
        """

        postedData = request.get_json()
        email = postedData["email"]

        user = usersCollection.find_one({"email": email})

        if user is None:
            js = json.dumps(
                {
                    "message": "User with email" + email + " not found in database",
                    "success": False,
                }
            )

            response = Response(js, status=404, mimetype="application/json")
            return response

        else:

            js = json.dumps({"data": user["username"], "success": True})

            response = Response(js, status=200, mimetype="application/json")
            return response


class CreateProduct(Resource):
    def post(self):
        
        """
        API endpoint to create a product of a user
        
        """

        postedData = request.get_json()
        email = postedData['email']
        link = postedData['link']
        price = postedData['price']

        user = usersCollection.find_one({"email": email})

        if user:

            productDocument = {
                'email' : email, 
                'link' : link, 
                'price' : price
            }
            productCollection.insert_one(productDocument)

            js = json.dumps({'message' : 'Product created succesfully', 'success': True})
            response = Response(js, status=200, mimetype="application/json")
            return response

        else :
            js = json.dumps({'message' : 'User not found', 'success': False})
            response = Response(js, status=403, mimetype="application/json")
            return response




api.add_resource(CreateUser, "/signup")
api.add_resource(GetUserForLogin, "/signin")
api.add_resource(GetUserName, "/getuser")
api.add_resource(CreateProduct, "/createproduct")


@app.route("/")
def home():
    return "Welcome to API Home"


if __name__ == "__main__":
    app.run(debug=True)
