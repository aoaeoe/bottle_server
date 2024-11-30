# -*- coding:utf-8 -*-

from bottle import request
from core.resp import JsonResponse
from core.decorator import route


def get_data():
    d = {"key1": "value1", "key2": "value2", "key3": "value3"}
    return JsonResponse.success(data=d)


def echo_data():
    try:
        data = request.json
        if not data:
            raise ValueError("No JSON body found")
        return JsonResponse.success(data=data)
    except Exception as e:
        return JsonResponse.error(message=str(e))


@route('/api/http_test', method='GET')
def http_test():
    d = {"key1": "value1", "key2": "value2", "key3": "value3"}
    return JsonResponse.success(data=d)
