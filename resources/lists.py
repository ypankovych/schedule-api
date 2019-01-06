from flasgger import swag_from
from flask_restful import Resource

from common.utils import get_full
from common.config import groups_endpoint, teachers_endpoint


class AllGroups(Resource):

    @staticmethod
    @swag_from('../docs/all_groups.yaml')
    def get():
        return get_full(groups_endpoint), 200


class AllTeachers(Resource):

    @staticmethod
    @swag_from('../docs/all_teachers.yaml')
    def get():
        return get_full(teachers_endpoint), 200
