import json
from flask import Response


def list_to_array(list):
    array = []
    for i, element in enumerate(list):
        array.append(element.to_dict())
    return array


def custom_response(status, message, data=None):
    if data is None:
        response_message = {
            "status": status,
            "message": message,
        }
    else:
        response_message = {
            "status": status,
            "message": message,
            "data": data
        }
    response_message = json.dumps(response_message)
    return Response(response_message, mimetype='application/json', status=status)
