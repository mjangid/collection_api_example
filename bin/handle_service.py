# System Import
import sys
import logging

# Splunk import
from splunklib.client import connect
from utils import parse

__author__ = 'Manoj Jangid'
__version__ = '0.0.1'
__description__ = 'This is class is responsible for service authorization'


class ServiceHandle(object):
    def __init__(self, collection_name):
        try:
            '''
            There is multiple way to authenticate this
            '''
            logging.debug('Service Handle Initialized')
            opts = parse(sys.argv[1:], {}, '.splunkrc')
            opts.kwargs["owner"] = 'nobody'
            opts.kwargs["app"] = 'collection_api_example'
            opts.kwargs["username"] = 'admin'
            opts.kwargs["password"] = 'admin'
            self.service = connect(**opts.kwargs)
            self.collection = self.service.kvstore[collection_name]
        except:
            raise Exception('Initialization Error: %s' % (sys.exc_info()[0]))

    def get_collection_handle(self):
        return self.collection

    def get_service_handle(self):
        return self.service
