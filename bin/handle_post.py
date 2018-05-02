
# System Import
import sys
import json
import logging

# Application import
from query_parameters import QueryParameters


from handle_error import HandleError


__author__ = 'Manoj Jangid'
__version__ = '0.0.1'
__description__ = 'This is class is responsible for all Post operation'


class HandlePost(object):

    def __init__(self, collection, request):
        logging.debug(
            'Initialize HandlePost class with request=%s' % (request))
        self.request = request
        self.collection = collection

    def post(self):
        data = {}
        raw = self.request['payload']
        fields = raw.split('&')
        for keyVal in fields:
            key, value = keyVal.split('=')
            data[key] = value

        try:
            response = self.collection.data.insert(json.dumps(data))
        except:
            error = HandleError(self.collection, self.request)
            return error.execute()

        data['_key'] = response['_key']
        self.request['body'] = data

        return {'payload': self.request, 'status': 200}

    def execute(self):
        return self.post()
