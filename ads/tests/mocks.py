"""
Mock responses
"""

import json

from httpretty import HTTPretty as OriginalHTTPretty
from .stubdata.solr import example_solr_response
from .stubdata.metrics import example_metrics_response
from .stubdata.export import example_export_response

try:
    from requests.packages.urllib3.contrib.pyopenssl import inject_into_urllib3, extract_from_urllib3
    pyopenssl_override = True
except:
    pyopenssl_override = False


class MyHTTPretty(OriginalHTTPretty):
    """
    Taken from: https://github.com/mredar/harvester/commit/228e9c3319ac6de651fc44d977efc3cc7b67e092

    pyopenssl monkey-patches the default ssl_wrap_socket() function in the 'requests' library,
    but this can stop the HTTPretty socket monkey-patching from working for HTTPS requests.

    Our version extends the base HTTPretty enable() and disable() implementations to undo
    and redo the pyopenssl monkey-patching, respectively.
    """

    @classmethod
    def enable(cls):
        OriginalHTTPretty.enable()
        if pyopenssl_override:
            # Take out the pyopenssl version - use the default implementation
            extract_from_urllib3()

    @classmethod
    def disable(cls):
        OriginalHTTPretty.disable()
        if pyopenssl_override:
            # Put the pyopenssl version back in place
            inject_into_urllib3()


HTTPretty = MyHTTPretty


class HTTPrettyMock(object):
    """
    httpretty context manager scaffolding
    """

    def __enter__(self):
        HTTPretty.enable()

    def __exit__(self, etype, value, traceback):
        """
        :param etype: exit type
        :param value: exit value
        :param traceback: the traceback for the exit
        """
        HTTPretty.reset()
        HTTPretty.disable()


class MockResponse(object):
    """
    mock for a simple response with a given body
    """
    def __init__(self, body):
        self.text = body

    def json(self):
        return json.loads(self.text)


class MockApiResponse(HTTPrettyMock):
    """
    context manager than mocks an static adsws-api response
    """
    limit = 400
    remaining = 398
    reset = 1436313600

    @property
    def remains(self):
        MockApiResponse.remaining -= 1
        return MockApiResponse.remaining

    def __init__(self, api_endpoint):
        self.api_endpoint = api_endpoint

        HTTPretty.register_uri(
            HTTPretty.GET,
            self.api_endpoint,
            body='''{"status": "online", "app": "adsws.api"}''',
            content_type="application/json",
            adding_headers={
                'X-RateLimit-Limit': MockApiResponse.limit,
                'X-RateLimit-Remaining': self.remains,
                'X-RateLimit-Reset': MockApiResponse.reset
            }
        )


class MockSolrResponse(HTTPrettyMock):
    """
    context manager that mocks a Solr response
    """
    def __init__(self, api_endpoint):
        """
        :param api_endpoint: name of the API end point
        """

        self.api_endpoint = api_endpoint

        def request_callback(request, uri, headers):
            """
            :param request: HTTP request
            :param uri: URI/URL to send the request
            :param headers: header of the HTTP request
            :return: httpretty response
            """

            resp = json.loads(example_solr_response)

            # Mimic the start, rows behaviour
            rows = int(
                request.querystring.get(
                    'rows', [len(resp['response']['docs'])]
                )[0]
            )
            rows = min(rows, 300)
            start = int(request.querystring.get('start', [0])[0])
            try:
                resp['response']['docs'] = resp['response']['docs'][start:start+rows]
            except IndexError:
                resp['response']['docs'] = resp['response']['docs'][start:]
            resp['responseHeader']['params']['rows'] = rows

            # Mimic the filter "fl" behaviour
            fl = request.querystring.get('fl', ['id'])
            resp['response']['docs'] = [
                {field: doc.get(field) for field in fl}
                for doc in resp['response']['docs']
            ]
            resp['responseHeader']['params']['fl'] = fl

            # Mimic cursor behavior if specified
            if request.querystring.get('cursorMark'):
                resp['nextCursorMark'] = "AoIH///3RmWrhAAjMTY0"

            return 200, headers, json.dumps(resp)

        HTTPretty.register_uri(
            HTTPretty.GET,
            self.api_endpoint,
            body=request_callback,
            content_type="application/json"
        )


class MockMetricsResponse(HTTPrettyMock):
    """
    context manager that mocks a metrics service response
    """
    def __init__(self, api_endpoint):
        """
        :param api_endpoint: name of the API end point
        """

        self.api_endpoint = api_endpoint

        HTTPretty.register_uri(
            HTTPretty.POST,
            self.api_endpoint,
            body=example_metrics_response,
            content_type="application/json"
        )


class MockExportResponse(HTTPrettyMock):
    """
    context manager that mocks an export service response
    """
    def __init__(self, api_endpoint):
        """
        :param api_endpoint: name of the API end point
        """

        self.api_endpoint = api_endpoint

        HTTPretty.register_uri(
            HTTPretty.POST,
            self.api_endpoint,
            body=example_export_response,
            content_type="application/json"
        )
