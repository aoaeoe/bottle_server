# -*- coding:utf-8 -*-

import os
import importlib
from bottle import Bottle


def register_all_routes(app: Bottle, base_module="api.v1"):
    base_dir = os.path.join(os.path.dirname(__file__), "..", *base_module.split("."))  # 基础模块的目录
    for root, _, files in os.walk(base_dir):
        for filename in files:
            if filename.endswith(".py") and filename != "__init__.py":
                # 构造模块路径
                relative_path = os.path.relpath(root, base_dir).replace(os.sep, ".")
                module_name = f"{base_module}.{relative_path}.{filename[:-3]}" if relative_path != "." else f"{base_module}.{filename[:-3]}"
                try:
                    module = importlib.import_module(module_name)  # 动态导入模块
                    for attr_name in dir(module):  # 模块的所有函数
                        obj = getattr(module, attr_name)
                        if callable(obj) and hasattr(obj, "route_config"):
                            route_config = obj.route_config
                            app.route(route_config["path"], route_config["method"], obj)  # 动态注册路由
                except Exception as e:
                    print(f"Failed to load routes from {module_name}: {e}")
