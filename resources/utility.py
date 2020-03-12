import json


def list_to_json(list):
    array = []
    for i, element in enumerate(list):
        array.append(element.to_dict())
    array = json.dumps(array)
    return array