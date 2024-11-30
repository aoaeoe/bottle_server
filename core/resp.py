# -*- coding:utf-8 -*-

from bottle import response
import json


class JsonResponse:
    @staticmethod
    def success(data=None, message="Success", code=0):
        return JsonResponse._build_response(data, message, code)

    @staticmethod
    def error(message="Error", code=1, data=None, status=200):
        return JsonResponse._build_response(data, message, code, status)

    @staticmethod
    def _build_response(data, message, code, status=200):
        response.content_type = "application/json"
        response.status = status
        return json.dumps({
            "code": code,
            "message": message,
            "data": data
        })
