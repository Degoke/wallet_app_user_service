from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        print(response.data)
        # if isinstance(exc, ValidationError):
        #     print(response.data['non_field_errors'])
        # else:
        response.data = {"status": "error", "message": response.data['detail']}
    
    return response

class InvalidUrl(APIException):
    status_code = 400
    default_detail = "The Url you have entered is invalid"
    default_code = 'bad_request'

class BadRequest(APIException):
    status_code = 400
    default_code = 'bad_request'

    def __init__(self, details):
        super().__init__(detail=details)
