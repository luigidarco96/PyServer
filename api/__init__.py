from flask_restplus import Api

authorizations = {
    'apiKey': {
        'type' : 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}


api = Api(version='1.0',
          title='PiServer API',
          description='A Flask Server powered API',
          authorizations=authorizations)
