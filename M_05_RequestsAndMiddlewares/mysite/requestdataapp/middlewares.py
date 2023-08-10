import time

from django.http import HttpRequest, HttpResponse


class TimeRequestsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.ip_time = {}

    def __call__(self, request: HttpRequest) -> HttpResponse:
        update_frequency = 15
        ip = request.META['REMOTE_ADDR']
        request_time = round(time.time(), 0)

        if request_time - self.ip_time.get(ip, 0) > update_frequency:
            self.ip_time[ip] = request_time
            response = self.get_response(request)
        else:
            response = HttpResponse('Request limit exceeded', status=400)

        return response
