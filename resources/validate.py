from functools import partial

from flasgger import swag_from
from flask_restful import Resource
from webargs import fields, ValidationError
from webargs.flaskparser import use_kwargs

from common.utils import get_full


def validate_kind(kind, obj):
    if obj.upper() in [x[kind[:-1]].upper() for x in get_full(kind)]:
        return True
    raise ValidationError(f'{kind[:-1]} does not exists')


class GroupValidate(Resource):
    args = {
        'group': fields.Str(required=True, validate=partial(validate_kind, 'groups'))
    }

    @staticmethod
    @use_kwargs(args)
    @swag_from('../docs/group_validate.yaml')
    def get(group):
        for i in get_full('groups'):
            if i['group'] == group.upper():
                return i, 200


class TeacherValidate(Resource):
    args = {
        'teacher': fields.Str(required=True, validate=partial(validate_kind, 'teachers'))
    }

    @staticmethod
    @use_kwargs(args)
    @swag_from('../docs/teacher_validate.yaml')
    def get(teacher):
        for i in get_full('teachers'):
            if i['teacher'].upper() == teacher.upper():
                return i, 200
