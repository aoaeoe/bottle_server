# -*- coding:utf-8 -*-

import signal
# from bottle import run
from gevent import monkey
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from api.main import app

monkey.patch_all()


def graceful_shutdown(server):
    """优雅关闭服务器"""
    print("\nShutting down server gracefully...")
    server.stop(timeout=5)  # 给服务器一些时间完成当前请求
    print("Server stopped.")


if __name__ == '__main__':
    # run(app=app, host='localhost', port=8080, debug=True, reloader=True)

    server = WSGIServer(("0.0.0.0", 8080), app, handler_class=WebSocketHandler)
    signal.signal(signal.SIGINT, lambda sig, frame: graceful_shutdown(server))
    print("Server started at http://127.0.0.1:8080")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        graceful_shutdown(server)
