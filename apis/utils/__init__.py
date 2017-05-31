from flask_restplus import reqparse

pagination = reqparse.RequestParser()
pagination.add_argument('page', type=int, required=False, default=1, help='Page number')
pagination.add_argument('per_page', type=int, required=False, choices=[10,20,30,40,50], default=10, help='Items per page')
