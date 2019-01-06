import os

from flasgger import Swagger
from flask import Flask, redirect
from flask_restful import Api
from webargs.flaskparser import parser, abort

from common.config import template
from resources.lists import AllGroups, AllTeachers
from resources.schedule import Group, Teacher

app = Flask(__name__)
app.config['RESTFUL_JSON'] = {
    'ensure_ascii': False
}

api = Api(app)
swagger = Swagger(app, template=template)


@app.route('/')
def redirect_to_docs():
    return redirect('/apidocs')


@parser.error_handler
def handle_request_parsing_error(err, *args):
    abort(422, errors=err.messages)


api.add_resource(Group, '/groups/schedule')
api.add_resource(Teacher, '/teachers/schedule')
api.add_resource(AllGroups, '/groups/all')
api.add_resource(AllTeachers, '/teachers/all')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 5000))
