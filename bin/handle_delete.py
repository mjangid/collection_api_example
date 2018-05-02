
# System Import
import json
import logging

# Splunk import
from splunklib.binding import ResponseReader as RR

# Application import
from handle_error import HandleError


__author__ = 'Manoj Jangid'
__version__ = '0.0.1'
__description__ = 'This is class is responsible for all delete operation'


class HandleDelete(object):

    def __init__(self, collection, request):
        logging.debug(
            'Initialize HandleDelete class with request=%s' % (request))
        self.request = request
        self.collection = collection

    def delete(self):
        value = self.request.get('path_info')
        if value:
            logging.debug('path_info=%s' % self.request.get('path_info'))
        else:
            logging.debug('path_info key is missing')

        data = {}
        data['_key'] = value
        try:
            response = self.collection.data.delete(json.dumps(data))
        except:
            error = HandleError(self.collection, self.request)
            return error.execute()

        return {'payload': self.request, 'status': response['status']}

    def execute(self):
        return self.delete()
