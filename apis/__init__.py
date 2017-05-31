from flask_restplus import Api

from .users_ns import api as ns1

api = Api(
    title='Qualibrate Foundation API',
    version='1.0',
    description='Testing, documentation and training seamless framework'
)

api.add_namespace(ns1)
