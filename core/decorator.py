# -*- coding:utf-8 -*-

def route(path, method="GET"):
    def decorator(func):
        func.route_config = {"path": path, "method": method}  # 保存路由信息
        return func
    return decorator
