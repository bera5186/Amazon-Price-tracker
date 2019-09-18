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
    conn = MongoClient('mongodb://localhost:27017')
    db   = conn.amazon_price_tracker
    productCollection = db.products
    usersCollection = db.users
    print('db connected')
except:
    print('error connecting to db')


class CreateUser(Resource):
    def post(self):

        """
        Create a user in a database
        
        """
        postedData = request.get_json()
        email = postedData["email"]
        userName = postedData["username"]
        password = postedData["password"]

        checkedEmail = usersCollection.find_one({'email' : email})

        if checkedEmail is None:
            hashedPassword = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(8))

            userDocument = {
                "email" : email,
                "password" : hashedPassword,
                "username" : userName

            }

            usersCollection.insert_one(userDocument)

            try:
                js = json.dumps({
                    "message" : "User succesfully created",
                    "success" : True
                })
                response = Response(js, status=200, mimetype='application/json')
            except:
                js = json.dumps({
                    "message" : "Cannot create a user",
                    "success" : False
                })
                response = Response(js, status=500, mimetype='application/json')

            return response
        else:
            js = json.dumps({
                "message" : "Email already taken",
                "success" : False
            })

            response = Response(js, status=400, mimetype='application/json')
            return response
        

        
        


class GetUser(Resource):
    def get(self):
        """
        Check for a user in database
        
        """

        postedData = request.get_json()
        email = postedData["email"]
        password = postedData["password"]






api.add_resource(CreateUser, "/signup")


@app.route('/')
def home():
    return "hello world"


if __name__ == '__main__':
    app.run(debug=True)



