# -*- coding:utf-8 -*-

from api.v1.http.handlers import get_data, echo_data
from api.v1.sse.sse import events
from api.v1.ws.ws import websocket_handler
from api.v1.user.user import create, get, update, list_users
# 路由表
ROUTE_CONFIG = [
    {
        "path": "/api/v1/data",
        "method": "GET",
        "handler": get_data,
    },
    {
        "path": "/api/v1/echo",
        "method": "POST",
        "handler": echo_data,
    },
    # sse
    {
        "path": "/api/v1/sse",
        "method": "GET",
        "handler": events,
    },
    # ws
    {
        "path": "/api/v1/ws",
        "method": "GET",
        "handler": websocket_handler,
    },
    # user
    {
        "path": "/api/v1/user",
        "method": "POST",
        "handler": create,
    },
    {
        "path": "/api/v1/user",
        "method": "GET",
        "handler": get,
    },
    {
        "path": "/api/v1/user",
        "method": "PUT",
        "handler": update,
    },
    {
        "path": "/api/v1/users",
        "method": "GET",
        "handler": list_users,
    },
]
