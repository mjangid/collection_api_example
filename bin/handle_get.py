
# System Import
import sys
import json
import logging

# Splunk import
from splunklib.binding import ResponseReader

# Application import
from query_parameters import QueryParameters
from handle_error import HandleError


__author__ = 'Manoj Jangid'
__version__ = '0.0.1'
__description__ = 'This is class is responsible for all Get operation'

class HandleGet(object):

    def __init__(self, collection, request):
        logging.info('Initialize HandleGet class with request=%s' % (request))
        self.request = request
        self.collection = collection
        self.query_params = request['query']

    def get_filters(self):
        data = {}
        params = QueryParameters(self.query_params)
        param_list = json.loads(params.get())

        for param in param_list:
            data[param] = param_list[param]

        logging.info('filters=%s' % (json.dumps(data)))

        return json.dumps(data)

    def get(self):
        try:
            if len(self.query_params) > 0:
                response = self.collection.data.query(query=self.get_filters())
            else:
                response = self.collection.data.query()
            return response
        except:
            raise Exception(sys.exc_info()[0])

    # Customize your response
    def execute(self):
        try:
            self.request['body'] = self.get()        
            return {'payload': self.request, 'status': 200}
        except:
            error = HandleError(self.collection, self.request)
            return error.execute()

