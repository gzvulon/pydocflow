
def is_cfg_method(cfg_class, method):
    import inspect
    def fntype_sample(): pass
    is_method = type(fntype_sample) == type(method)
    if not is_method:
        return False
    fas = inspect.getfullargspec(method)
    if fas.annotations.get('cfg', None) == cfg_class:
        return True
    return False


def to_cfg_method(f):
    from functools import wraps
    @wraps(f)
    def _wrapper(self, *args, **kwargs):
        return f(self._cfg, *args, **kwargs)
    return _wrapper


def make_cfg_bond(cfg_class, methods):
    def ctor(self, cfg=None):
        self._cfg = cfg or cfg_class()

    _name = f"{cfg_class.__name__}Cli"
    _dict = {
        "string_val": "this is val1",
        "__init__": ctor,
    }
    _methods = {
        name: to_cfg_method(fnc)
        for name, fnc in methods.items()
        if is_cfg_method(cfg_class, fnc)
    }
    _dict.update(_methods)
    NewClass = type(_name, (object,), _dict)
    return NewClass


def make_cfg_bond_dict(cfg_class, methods):
    def ctor(self, **kw):
        """
        :param self:
        :param kw:
        :return:
        """
        self._cfg = cfg_class(**kw)

    _name = f"{cfg_class.__name__}Cli"
    _dict = {
        "string_val": "this is val1",
        "__init__": ctor,
    }
    _methods = {
        name: to_cfg_method(fnc)
        for name, fnc in methods.items()
        if is_cfg_method(cfg_class, fnc)
    }
    _dict.update(_methods)
    NewClass = type(_name, (object,), _dict)
    return NewClass