# -*- coding:utf-8 -*-

from bottle import request
from gevent import monkey
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler

monkey.patch_all()


def websocket_handler():
    ws = request.environ.get('wsgi.websocket')
    if not ws:
        return "WebSocket connection required!"
    try:
        while True:
            message = ws.receive()
            if message is None:
                break
            print(f"Received: {message}")
            ws.send(f"Echo: {message}")
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        ws.close()
