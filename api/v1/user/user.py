# -*- coding:utf-8 -*-

from bottle import request
from models.user import User
from core.resp import JsonResponse
from core.database import session
from core.base import jsonify
from core.decorator import route


@route('/api/get_data1234', method='GET')
def get_data():
    name = request.query.name
    if not name:
        return JsonResponse.error("Missing required parameter: 'name'")
    data = {"message": f"Hello, {name}!"}
    return JsonResponse.success(data)


@route('/api/echo123', method='POST')
def echo_data():
    try:
        data = request.json
        if not data:
            return JsonResponse.error("Missing JSON body")
        return JsonResponse.success({"received": data})
    except Exception as e:
        return JsonResponse.error(str(e))


def create():
    try:
        kw = request.json
        if not kw:
            raise ValueError("No JSON body found")
        User.create(**kw)
        return JsonResponse.success()
    except Exception as e:
        return JsonResponse.error(message=str(e))


def get():
    name = request.query.name
    age = request.query.age
    kw = {'name': name}

    data = session.query(User).filter(User.name == kw.get('name')).all()
    user_dicts = [jsonify(user) for user in data]
    print(user_dicts)
    return JsonResponse.success(user_dicts)


def list_users():
    data = session.query(User).all()
    user_dicts = [jsonify(user) for user in data]
    return JsonResponse.success(user_dicts)


def update():
    try:
        kw = request.json
        if not kw:
            raise ValueError("No JSON body found")
        print(type(kw))
        session.query(User).filter(User.name == kw.get('name')).update(kw)
        session.commit()
        return JsonResponse.success(data=kw)
    except Exception as e:
        # session.rollback()
        return JsonResponse.error(message=str(e))


def delete():
    ...
