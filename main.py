from flask import Flask, request, make_response
from flask_restful import Resource, Api
from flask_cors import CORS
from encoder import encode, decode

app = Flask(__name__)
CORS(app)
api = Api(app)

class Encode(Resource):
    def post(self):
        try:
            response = make_response(encode(request.get_data().decode("utf-8")), 200)
        except UnicodeDecodeError:
            response = make_response("Error: body is not valid unicode", 400)
        response.mimetype = "text/plain"
        return response

class Decode(Resource):
    def post(self):
        # check if body is valid unicode
        try:
            text = request.get_data().decode("utf-8")
        except UnicodeDecodeError:
            response = make_response("Error: body is not valid unicode", 400)
            response.mimetype = "text/plain"
            return response

        # check if decode was successful
        try:
            response = make_response(decode(text), 200)
        except ValueError as e:
            response = make_response(str(e), 400)
        response.mimetype = "text/plain"
        return response

api.add_resource(Encode, "/v1/encode")
api.add_resource(Decode, "/v1/decode")

if __name__ == "__main__":
    app.run()