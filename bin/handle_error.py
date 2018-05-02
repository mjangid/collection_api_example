
# System Import
import logging
__author__ = 'Manoj Jangid'
__version__ = '0.0.1'
__description__ = 'Custom Error Handler'


class HandleError(object):

    def __init__(self, collection, request):
        logging.debug('Initialize HandleError class with request=%s' % (request))
        self.request = request
        self.collection = collection

    def error(self):
        return {'payload': 'Server Error - Contact to Support', 'status': 500}

    def execute(self):
        self.error()