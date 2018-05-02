
# System Import
import sys
import json
import logging

# Application import
from handle_error import HandleError

__author__ = 'Manoj Jangid'
__version__ = '0.0.1'
__description__ = 'This is class is responsible for all Post operation'


class HandlePut(object):

    def __init__(self, collection, request):
        self.request = request
        self.collection = collection

    def put(self):
        req = self.request
        _key, _value = None, None
        json_obj = {}
        try:
            form_data = req['form']
            for data in form_data:
                key = data[0]
                val = data[1]
                if key == '_key':
                    _key = key
                    _value = val
                else:
                    json_obj[key] = val

            if _key == None:
                logging.debug('invalid input (_key is missing) data=%s' %
                              (json.dumps(json_obj)))
                error = HandleError(self.collection, self.request)
                return error.execute()

            query = {}
            query['_key'] = _value.encode('utf-8')

            response = self.collection.data.query(query=json.dumps(query))[0]

            logging.debug('New Value=%s' % (json.dumps(json_obj)))
            logging.debug('Old Value=%s' % (json.dumps(response)))

            try:
                logging.debug('Updating KV Store _key=%s data=%s' %
                              (_value, json.dumps(json_obj)))
                response = self.collection.data.update(
                    _value, json.dumps(json_obj))
            except:
                error = HandleError(self.collection, self.request)
                return error.execute()

            self.request['body'] = response

            logging.debug('end=put_operation')
            return {'payload': self.request, 'status': 200}

        except:
            logging.debug('error=%s' % (sys.exc_info()[0]))

    def execute(self):
        return self.put()
