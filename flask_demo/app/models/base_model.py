from ..base import db
import json
from datetime import datetime

class BaseModel(db.Model):
    """ Basic Model
    """
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now())

    __abstract__ = True

    client_exclude_attrs = ["deleted"]
    hash_id_map = dict()
    views = None

    @classmethod
    def add_view(cls, name, attrs = [], exclude_attrs=[]):
        if not cls.views:
            cls.views = {}
        if len(attrs) == 0 and len(exclude_attrs) == 0:
            raise ValueError("Views must contains at least 1 attribute")
        if len(attrs) > 0 and len(exclude_attrs) > 0:
            raise ValueError("Views can't contains both attrs and exclude_attrs at same time")
        u = {}
        if len(exclude_attrs) > 0:
            u[name] = ModelView(cls, exclude_attrs, True)
        else:
            u[name] = ModelView(cls, attrs, False)
        cls.views.update(u)

    def update(self, data:dict):
        for key, value in data.items():
            setattr(self, key, value)

    def get_attr_dict(self):
        d = dict()
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d

    def to_dict(self, view=None, excludes = [], relation_keys=[]):
        """ 以 dict 形式返回 model 数据
            会应用 Model.hash_id_map 和 Model.client_exclude_attrs 中的设置

            @view : str
            要使用的 ModelView 的名称

            @excludes : list[str]
            要忽略的属性, 可以与view同时使用

            @relation_keys : list[str]
            包含的 relation_keys 的列表
            必须传入已经在 Model 中声明过的 relation_key
            接受以下形式:
                "relation_key"
                "relation_key:view_name"
        """
        if view:
            if view not in self.views:
                fmt = "Model '%s' doesn't have view named '%s'"
                raise KeyError(fmt % (type(self).__name__, view))
            d = self.views[view].render(self)
        else:
            d = dict()
            for column in self.__table__.columns:
                d[column.name] = getattr(self, column.name)
        # 处理 hash_id 对应关系
        for name_id,name_hash_id in type(self).hash_id_map.items():
            if name_hash_id not in d:
                continue
            d[name_id] = d[name_hash_id]
            del d[name_hash_id]

        # 处理去除建
        remove_keys = []
        for key,value in d.items():
            if key in type(self).client_exclude_attrs or key in excludes:
                remove_keys.append(key)
            elif value is None:
                if isinstance(value, int) or isinstance(value, float):
                    d[key] = 0
                elif isinstance(value, bool):
                    d[key] = False
                else:
                    d[key] = ""

        for key in remove_keys:
            del d[key]

        # 把所有datetime类型转换成整形timestamp
        for key,value in d.items():
            if isinstance(value,datetime):
                d[key] = int(value.timestamp())

        # 递归处理 relation_key
        for key in relation_keys:
            if key.startswith("?"):
                key = key[1:]
                optional = True
            else:
                optional = False
            parts = key.split(":")
            key = parts[0]
            view_name = parts[1] if len(parts) == 2 else None
            model = getattr(self, key)
            if isinstance(model, list):
                d[key] = [i.to_dict(view=view_name) for i in model]
            elif isinstance(model, BaseModel):
                d[key] = model.to_dict(view=view_name)
            else:
                if not optional:
                    raise KeyError("can't find relation key %s" % key)
                else:
                    #TODO 可选relation key 为空时如何处理？
                    pass

        return d

    def to_json(self, excludes = []):
        """ return as json string
        """
        return json.dumps(self.to_dict(excludes))

class HashIdModel(BaseModel):
    """ model that contains one or more hash_ids
    """

    hash_id = db.Column(db.String(12), index=True, unique=True)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now())

    __abstract__ = True

    # to_dict 方法调用时
    # 此dicit中规定的id将会被对应hash_id替代
    # 同时hash_id会被删除
    hash_id_map = {
        "id" : "hash_id"
    }

class ModelView:
    """ ModelView 规定了一个 Model 中的哪些属性会被发送给客户端
        一个 Model 可以有多个 ModelView

        view 可以正确处理 hash_id, 因此声明时属性应该是 hash_id 映射后的属性
        例如 应该写 id 而非 hash_id

        ModelView 中 *不可以* 包含 client_exclude_attrs 中的 key
    """
    def __init__(self, model_cls, attrs, exclude_type=False):
        for a in attrs:
            try:
                attr = getattr(model_cls, a)
            except AttributeError as e:
                hash_id_mapped_key = model_cls.hash_id_map.get(a)
                if hash_id_mapped_key:
                    attr = getattr(model_cls, hash_id_mapped_key)
                else:
                    raise e
            if not attr:
                fmt = "%s is neigher Column or Relation Key of class %s"
                raise KeyError(fmt % (a, model_cls.__name__))
            if a in model_cls.client_exclude_attrs:
                fmt = "%s was in %s's client_exclude_attrs"
                raise KeyError(fmt % (a, model_cls.__name__))

        self.attrs = attrs
        self.exclude_type = exclude_type

    def render(self, model):
        """ 根据 view 中的 key 来筛选 model
            如果声明中没有包含, 则不会触发取值操作
            因此可以安全的处理声明为 deferred 的属性
            返回新的 dict
        """
        d = {}
        c = type(model)
        reversed_hash_id_map = {}
        for k,v in c.hash_id_map.items():
            reversed_hash_id_map[v] = k

        if self.exclude_type:
            # 除去模式
            for column in model.__table__.columns:
                n = column.name
                if n in c.client_exclude_attrs \
                or n in self.attrs \
                or reversed_hash_id_map.get(n) in self.attrs:
                    continue
                d[column.name] = getattr(model, column.name)
        else:
            # 包含模式p
            for column in model.__table__.columns:
                n = column.name
                if n in c.client_exclude_attrs:
                    continue
                if n in self.attrs\
                or reversed_hash_id_map.get(n) in self.attrs:
                    d[column.name] = getattr(model, column.name)

        return d
