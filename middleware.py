from django import http


class AllowAllXHROrigins(object):
    """Allow all origins and methods for XHR requests

    Mainly this is so we can use AJAX from jenkins without much effort

    Reference:

        https://developer.mozilla.org/en-US/docs/Web/HTTP/Access_control_CORS

    """
    METHODS = ','.join(['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS'])

    def process_request(self, request):
        # Intercept preflight requests and respond with all methods/origins
        if 'HTTP_ACCESS_CONTROL_REQUEST_METHOD' in request.META:
            # This is a reflight request, we can construct the response right here
            response = http.HttpResponse()
            response['Access-Control-Allow-Origin'] = '*'
            response['Access-Control-Allow-Methods'] = self.METHODS
            return response

    def process_response(self, request, response):
        # Add cors headers, rudely overwriting whatever might have been
        # there to allow all origins/methods
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = self.METHODS
        return response
