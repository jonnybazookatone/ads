"""
interfaces to the adsws biblib service
"""

import json
import six

from .base import APIResponse, BaseQuery
# from .config import METRICS_URL
#
#
# class MetricsResponse(APIResponse):
#     """
#     Data structure that represents a response from the ads metrics service
#     """
#     def __init__(self, http_response):
#         self._raw = http_response.text
#         self.metrics = http_response.json()
#


class Library():
    """
    A container for a collection of Articles, and also meta data
    """

    def __init__(self, **kwargs):
        """
        :param kwargs: Set object attributes from kwargs
        """

        self._raw = kwargs
        for key, value in six.iteritems(kwargs):
            setattr(self, key, value)

    def __eq__(self, other):
        if self._raw.get('id') is None or other._raw.get('id') is None:
            raise TypeError('Cannot compare libraries without ids')

        return self._raw['id'] == other._raw['id']

    # def __ne__(self, other):
    #     return not self.__eq__(other)


class LibraryQuery(BaseQuery):
    def __init__(self):
        pass

    def execute(self):
        pass


#
# class MetricsQuery(BaseQuery):
#     """
#     Represents a query to the adsws metrics service
#     """
#
#     HTTP_ENDPOINT = METRICS_URL
#
#     def __init__(self, bibcodes):
#         """
#         :param bibcodes: Bibcodes to send to in the metrics query
#         :type bibcodes: list or string
#         """
#         self.response = None  # current MetricsResponse object
#         if isinstance(bibcodes, six.string_types):
#             bibcodes = [bibcodes]
#         self.bibcodes = bibcodes
#         self.json_payload = json.dumps({"bibcodes": bibcodes})
#
#     def execute(self):
#         """
#         Execute the http request to the metrics service
#         """
#         self.response = MetricsResponse.load_http_response(
#             self.session.post(self.HTTP_ENDPOINT, data=self.json_payload)
#         )
#         return self.response.metrics