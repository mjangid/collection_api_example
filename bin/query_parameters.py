import json
import logging

__author__ = 'Manoj Jangid'
__version__ = '0.0.1'
__description__ = 'Custom Python class to handle the query parameter and return json array'


class QueryParameters(object):
    json_qp = {}

    def __init__(self, qp):
        logging.info('Query parameter class initialized with query_parameter=%s type=%s count=%s' % (
            qp, type(qp), len(qp)))
        self.json_qp = {}
        query_parameters = qp[0]

        qp_size = len(query_parameters)

        for count in range(0, qp_size):
            if count == 0:
                if str(query_parameters[count]) == str('query'):
                    logging.info('query_keyword=true filter=%s' %
                                 (query_parameters[0]))
                else:
                    logging.info('invalid query parameter %s=%s' %
                                 (str(query_parameters[0]), str('query')))
                    raise Exception(
                        'Error in Query parameters, please use correct way to pass')
            else:
                filters = query_parameters[count]
                filters = filters.encode("utf-8")
                coma_sep = filters.split(',')
                for filter in coma_sep:
                    key, value = filter.split(':')
                    self.json_qp[key] = value
                logging.info('Formatted Query String Parameters=%s' %
                             (json.dumps(self.json_qp)))

    def get(self):
        return json.dumps(self.json_qp)

    def getValue(self, key):
        return self.json_qp[key]
