# System import
import os
import sys
import json
import logging
import time

# Append PYTHONPATH so script will load corresponding library
splunk_home = os.getenv('SPLUNK_HOME')
sys.path.append(splunk_home + '/etc/apps/collection_api_example/bin/')
sys.path.append(splunk_home + '/etc/apps/collection_api_example/bin/utils/')
sys.path.append(
    splunk_home + '/etc/apps/collection_api_example/bin/splunklib/')


# Splunk Import
from splunk.persistconn.application import PersistentServerConnectionApplication
from splunklib.binding import ResponseReader
from utils import parse

# Local import
from query_parameters import QueryParameters
from handle_delete import HandleDelete
from handle_get import HandleGet
from handle_put import HandlePut
from handle_post import HandlePost
from handle_error import HandleError
from handle_service import ServiceHandle


__author__ = 'Manoj Jangid'
__version__ = '0.0.1'
__description__ = 'Collection ReST Resource'


if sys.platform == "win32":
    import msvcrt
    # Binary mode is required for persistent mode on Windows.
    msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY)
    msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
    msvcrt.setmode(sys.stderr.fileno(), os.O_BINARY)


class CollectionHandler(PersistentServerConnectionApplication):
    collection = None

    def __init__(self, command_line, command_arg):
        PersistentServerConnectionApplication.__init__(self)

    def handle(self, payload):
        logging.debug('begin=handle_method request=%s' % (payload))
        response = {}
        try:
            # get the http method
            json_data = json.loads(payload)
            method = json_data['method']

            # get the collection name
            try:
                rest_path = json_data['rest_path']
                collection_name = rest_path.replace("/", "")

            except:
                logging.error('error_message=%s' % (sys.exc_info()[0]))

            try:
                service_handle = ServiceHandle(collection_name)
                collection = service_handle.get_collection_handle()
            except:
                logging.error(
                    'Unable to get service handle, please contact to support')

        except:
            raise Exception('handle: %s' % (sys.exc_info()[0]))

        if method == 'GET':
            get = HandleGet(collection, json_data)
            response = get.execute()
        elif method == 'PUT':
            put = HandlePut(collection, json_data)
            response = put.execute()
        elif method == 'POST':
            post = HandlePost(collection, json_data)
            response = post.execute()
        elif method == 'DELETE':
            delete = HandleDelete(collection, json_data)
            response = delete.execute()
        else:
            error = HandleError(collection, json_data)
            response = error.execute()

        logging.debug('end=handle_method')

        return response
