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
        print('Исходные данные хранилища адресов клиентов', self.ip_time)
        print('Поступил запрос')
        print('Время запроса', request_time)
        print('IP адрес клиента', ip)
        print('=======================')
        if request_time - self.ip_time.get(ip, 0) > update_frequency:
            print('Запрос успешно обработан, прошло более 15 секунд')
            self.ip_time[ip] = request_time
            response = self.get_response(request)

        else:
            print('Ошибка! Запрос не обработан. Прошло менее 15 секунд.')
            response = HttpResponse('Request limit exceeded', status=400)
        print('Данные хранилища адресов после обработки запроса', self.ip_time)
        print('~~~~~~~~~~~~~~~~~~~~~')
        return response
