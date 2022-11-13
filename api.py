from flask import Flask
from flask_restful import Resource, Api, reqparse, abort

app = Flask(__name__)
api = Api(app)


post_args = reqparse.RequestParser()
post_args.add_argument('Name', type=str, required = True)
post_args.add_argument('Age', type=str, required = True)
post_args.add_argument("Father's Name", type=str, required = True)
post_args.add_argument('State', type=str, required = True)


class ELectoral(Resource):
    def post(self):
        args = post_args.parse_args()
        return args['Name']

api.add_resource(ELectoral, '/electoral')

if __name__ == '__main__':
    app.run(debug = True)