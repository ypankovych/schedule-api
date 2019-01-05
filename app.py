from flasgger import Swagger
from flask import Flask, redirect
from flask_restful import Api
from webargs.flaskparser import parser, abort
import os

from resources.schedule import Group, Teacher

app = Flask(__name__)
app.config['RESTFUL_JSON'] = {
    'ensure_ascii': False
}
app.config['SWAGGER'] = {
    'title': 'Schedule API',
    'uiversion': 3,
    'description': ''
}

api = Api(app)
swagger = Swagger(app)


@app.route('/')
def redirect_to_docs():
    return redirect('/apidocs')


@parser.error_handler
def handle_request_parsing_error(err, *args):
    abort(422, errors=err.messages)


api.add_resource(Group, '/groups/schedule')
api.add_resource(Teacher, '/teachers/schedule')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT'))
