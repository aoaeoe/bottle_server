# -*- coding:utf-8 -*-

class CorsMiddleware:
    def __init__(self, app, allow_origin="*", allow_methods=None, allow_headers=None):
        self.app = app
        self.allow_origin = allow_origin
        self.allow_methods = allow_methods or ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
        self.allow_headers = allow_headers or ['Origin', 'Content-Type', 'Accept', 'Authorization']

    def __call__(self, environ, start_response):
        def cors_start_response(status, headers, exc_info=None):
            headers.append(('Access-Control-Allow-Origin', self.allow_origin))
            headers.append(('Access-Control-Allow-Methods', ', '.join(self.allow_methods)))
            headers.append(('Access-Control-Allow-Headers', ', '.join(self.allow_headers)))
            headers.append(('Access-Control-Allow-Credentials', 'true'))
            return start_response(status, headers, exc_info)

        if environ['REQUEST_METHOD'] == 'OPTIONS':
            start_response('204 No Content', [
                ('Access-Control-Allow-Origin', self.allow_origin),
                ('Access-Control-Allow-Methods', ', '.join(self.allow_methods)),
                ('Access-Control-Allow-Headers', ', '.join(self.allow_headers))
            ])
            return []

        return self.app(environ, cors_start_response)

    def __getattr__(self, name):
        """代理Bottle的其他属性和方法"""
        return getattr(self.app, name)
