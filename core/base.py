# -*- coding:utf-8 -*-

import pytz
import decimal
from datetime import datetime
from sqlalchemy import Column, Integer
from core.database import session, Base

pytz.country_timezones('cn')
TZ = pytz.timezone('Asia/Shanghai')


def jsonify(model):
    return {c.name: getattr(model, c.name) for c in model.__table__.columns}


class FormatMixin:
    # 获取model对应实例的属性to_dict
    def to_dict(self):
        res = dict()

        for k in getattr(self, "__table__").columns:
            if isinstance(getattr(self, k.name), datetime):
                res[k.name] = getattr(self, k.name).strftime(
                    '%Y-%m-%d %H:%M:%S')
            elif isinstance(getattr(self, k.name), decimal.Decimal):
                res[k.name] = float(getattr(self, k.name))
            else:
                res[k.name] = getattr(self, k.name)

        return res

    @classmethod
    def get_columns(cls):
        return {k.name: 1 for k in getattr(cls, '__mapper__').c.values()}


class ModelMeta(FormatMixin):
    __table__ = None
    id = None

    def __init__(self, **kwargs):
        super(ModelMeta, self).__init__(**kwargs)

    @classmethod
    def create(cls, flush=False, **kwargs):
        return cls(**kwargs).save(flush=flush)

    def update(self, flush=False, **kwargs):
        kwargs.pop('id', None)
        for attr, value in kwargs.items():
            if value is not None:
                setattr(self, attr, value)
        if flush:
            return self.save(flush=flush)
        return self.save()

    def save(self, commit=True, flush=False):
        session.add(self)
        try:
            if flush:
                session.flush()
            elif commit:
                session.commit()
        except Exception as e:
            session.rollback()
            raise Exception(str(e))
        return self

    def delete(self, flush=False):
        session.delete(self)
        try:
            if flush:
                return session.flush()
            return session.commit()
        except Exception as e:
            session.rollback()
            raise Exception(str(e))

    def soft_delete(self, flush=False):
        # setattr(self, 'is_delete', True)
        setattr(self, 'is_delete', 1)
        self.save(flush=flush)

    @classmethod
    def batch_create(cls, args):
        try:
            if args and isinstance(args, list):
                obj_list = list()
                for kv in args:
                    obj_list.append(cls(**kv))
                session.bulk_save_objects(obj_list)  # session.add_all
                session.commit()
        except Exception as e:
            session.rollback()
            raise Exception(str(e))

    def batch_update(self):
        raise NotImplementedError

    @classmethod
    def batch_delete(cls, ids):  # todo 假批量
        for _id in ids:
            cls.get_by_id(_id).soft_delete(flush=True)

    @classmethod
    def get_by_id(cls, _id):
        if any((isinstance(_id, str) and _id.isdigit(),
                isinstance(_id, (int, float))), ):
            # return getattr(cls, 'query').filter(cls.id == int(_id)).first() or None
            return getattr(cls, 'query').get(int(_id)) or None

    @classmethod
    def get_by(cls, first=False, to_dict=True, field_list=None, exclude=None, deleted=False, **kwargs):
        field_list = field_list.strip().split(',') if field_list and isinstance(
            field_list, str) else (field_list or [])
        exclude = exclude.strip().split(',') if exclude and isinstance(
            exclude, str) else (exclude or [])

        keys = cls.get_columns()
        # 是columns里面的 不是columns里面的不要
        field_list = [k for k in field_list if k in keys]
        field_list = [k for k in keys if k not in exclude and not k.isupper()] if exclude else field_list  # 不是排除的字段&&是columns里面的
        field_list = list(filter(lambda x: '.' not in x, field_list))

        if hasattr(cls, 'deleted') and deleted is not None:  # todo deleted看是model情况-->int or bool
            kwargs['deleted'] = deleted

        if field_list:
            query = session.query(*[getattr(cls, k) for k in field_list])
            query = query.filter_by(**kwargs)
            result = [{k: getattr(q, k) for k in field_list} for q in query]  # {'字段名'：字段值} 和to_dict作用一样
        else:
            result = [q.to_dict if to_dict else q for q in getattr(
                cls, 'query').filter_by(**kwargs)]
        return result[0] if first and result else (None if first else result)

    @classmethod
    def get_by_like(cls, to_dict=True, **kwargs):
        query = session.query(cls)
        for k, v in kwargs.items():
            query = query.filter(getattr(cls, k).ilike('%{}%'.format(v)))
        return [q.to_dict if to_dict else q for q in query]


class SoftDeleteMixin:
    deleted = Column(Integer, index=True, default=0, comment='0未删除 1删除')


class TimestampMixin:
    created_at = Column(Integer, default=lambda: int(
        datetime.timestamp(datetime.now(TZ))), comment='插入时间')
    updated_at = Column(Integer, onupdate=lambda: int(
        datetime.timestamp(datetime.now(TZ))), comment='更新时间')


class SurrogatePK:
    # 指定"extend_existing"以重新定义现有表对象上的选项和列
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True)


class ModelMixin(Base, SurrogatePK, SoftDeleteMixin, TimestampMixin, ModelMeta):
    # 抽象类中只要用__abstract__ = True代替__tablename__即可完成一切工作,避免多重继承并拥有抽象基类,该指令用于不应映射到数据库表的抽象类
    __abstract__ = True


class Model(ModelMixin, ModelMeta):
    __abstract__ = True
