# -*- coding:utf-8 -*-

import os
import importlib
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

Base = declarative_base()

engine = create_engine('sqlite:///test.db', echo=True)  # ?check_same_thread=False
# Base.metadata.create_all(engine)

Session = scoped_session(sessionmaker(bind=engine, autocommit=False, autoflush=False))
session = Session()


def import_models():  # 动态导入模型
    base_dir = os.path.dirname(os.path.abspath(__file__))   # os.path.dirname(__file__)
    models_dir = os.path.join(base_dir, "models")

    for filename in os.listdir(models_dir):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = f"models.{filename[:-3]}"
            importlib.import_module(module_name)


def init_db():
    import_models()  # 迁移的时候打开  打包的时候关掉
    Base.metadata.create_all(bind=engine)
