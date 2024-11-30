# -*- coding:utf-8 -*-

import json
import sys
import logging
from bottle import Bottle, response, HTTPResponse
from logging.handlers import RotatingFileHandler
from router.routers import ROUTE_CONFIG
from core.database import init_db
from core.middlware import CorsMiddleware
from router.loader import register_all_routes


def create_app(config='settings'):
    app = Bottle()
    app = CorsMiddleware(app)
    init_db()
    # register_extensions(app)
    register_all_routes(app)   # 原生路由
    register_dynamic_routes(app)  # 可配置路由
    app = ErrorHandlingMiddleware(app)
    configure_logger(app)
    return app


def register_extensions(app):
    app.install()
    pass


def register_dynamic_routes(app):
    def register(path, method, handler):
        def wrapper(*args, **kwargs):
            try:
                result = handler(*args, **kwargs)
                if isinstance(result, (dict, list)):
                    response.content_type = 'application/json'
                    return json.dumps(result)
                return result
            except Exception as e:
                response.status = 400
                return {"status": "error", "message": str(e)}

        app.route(path, method=method)(wrapper)

    for route in ROUTE_CONFIG:
        register(route["path"], route["method"], route["handler"])


class ErrorHandlingMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        try:
            return self.app(environ, start_response)
        except Exception as e:
            print(str(e))
            error_message = {
                "code": 2000,
                "status": "error",
                "message": "An unexpected error occurred.",
            }
            response = HTTPResponse(
                body=error_message,
                status="error",
                content_type='application/json'
            )
            return response(environ, start_response)


def configure_logger(app, log_path="app.log", log_level="INFO", debug=False):
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(pathname)s %(lineno)d - %(message)s"
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.DEBUG if debug else log_level)

    file_handler = RotatingFileHandler(
        log_path, maxBytes=2**20, backupCount=5
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG if debug else log_level)

    app_logger = logging.getLogger("bottle_app")
    app_logger.setLevel(logging.DEBUG if debug else log_level)
    app_logger.addHandler(console_handler)
    app_logger.addHandler(file_handler)

    logging.basicConfig(level=logging.DEBUG if debug else log_level, handlers=[console_handler, file_handler])

    app.logger = app_logger
    app.logger.info("Logger configured successfully!")


app = create_app()
