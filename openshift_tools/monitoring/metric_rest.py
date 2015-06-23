#!/usr/bin/env python2
# vim: expandtab:tabstop=4:shiftwidth=4
"""
REST API for Zagg

Example usage:

     ml = []
     new_metric = UniqueMetric('a','b','c')
     ml.append(new_metric)
     new_metric = UniqueMetric('d','e','f')
     ml.append(new_metric)

     mr = MetricRest(host='172.17.0.27:8000')
     print mr.add_metric(ml)

"""

import requests
import json
from metricmanager import UniqueMetric

#Currently only one method is used.
#More will be added in the future, and this can be disabled
#pylint: disable=too-few-public-methods
class RestApi(object):
    """
    A base connection class to derive from.
    """

    # All args are required
    #pylint: disable=too-many-arguments
    def __init__(self, host=None, username=None, password=None, headers=None):

        if host is not None:
            self.host = host

        if username:
            self.username = username

        if password:
            self.password = password

        if headers:
            self.headers = headers

        self.base_uri = "http://" + host + "/"
        self.data = None

    def request(self, url, method, headers=None, params=None, data=None):
        """
        wrapper method for Requests' methods
        """
        if not url.startswith("https://") or not url.startswith("http://"):
            url = self.base_uri + url
        _headers = self.headers or {}
        if headers:
            _headers.update(headers)

        response = requests.request(
            auth=None, method=method, url=url, params=params, data=data,
            headers=_headers, timeout=130, verify=False
        )

        self.data = response.json()

        return (response.status_code, self.data)

#This class implements rest calls. We only have one rest call implemented
# add-metric.  More could be added here
#pylint: disable=too-few-public-methods
class MetricRest(object):
    """
    wrappers class around REST API so use can use it with python
    """
    rest = None
    user = None
    passwd = None

    def __init__(self, host, user=None, passwd=None, headers=None):

        self.rest = RestApi(host=host, username=user, password=passwd, headers=headers)

    def add_metric(self, unique_metric_list):
        """
        Add a list of UniqueMetrics (unique_metric_list) via rest
        """
        metric_list = []
        for metric in unique_metric_list:
            metric_list.append(metric.to_dict())

        headers = {'content-type': 'application/json; charset=utf8'}
        status, raw_response = self.rest.request(method='POST', url='metric',
                                                 data=json.dumps(unique_metric_list, default=lambda x: x.__dict__),
                                                 headers=headers)

        return (status, raw_response)

# This is for testing
#if __name__ == "__main__":
#
#    ml = []
#    new_metric = UniqueMetric('a','b','c')
#    ml.append(new_metric)
#    new_metric = UniqueMetric('d','e','f')
#    ml.append(new_metric)
#
#    mr = MetricRest(host='172.17.0.27:8000')
#    print mr.add_metric(ml)