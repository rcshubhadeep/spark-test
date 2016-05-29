from flask import Flask, request
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)


class MessagePost(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        return json_data

api.add_resource(MessagePost, '/api/events')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
