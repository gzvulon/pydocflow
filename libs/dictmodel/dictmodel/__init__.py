import copy
import json
import logging
from typing import List


try:
    from pathlib import Path
except (ImportError, SystemError):
    # for python 3.5 or rpi
    from pathlib2 import Path

try:
    # use ruamel if installed
    from ruamel.yaml import YAML
    yaml = YAML(typ='safe')
    yaml.width = 1024
    # yaml.default_flow_style = None
except (ImportError, SystemError):
    import yaml

from dictmodel.typing_helpers import get_subtypes


class DictField(object):
    """Field Descriptor used for name intellisense"""

    def __init__(self, 
                 value=None, 
                 help:str=None,
                 required=None, 
                 default=None,
                 on_access=None,
                 **kwargs):
        """
        :param value: default value
        :param help: purpose of field, short description
        :param required: currently only tag for futher use
        :param default: factory method, custom constructor,
                        that will be called if field is not initialized
                        and its return value will be assigned to field
        :param on_access: if True then on access to field
                          in case if field is not initialized
                          it will autocreate value for field using its type.
                          field shoud have a type hint 
                          (any real type or List[T]/Dict[TK, TV] from typing)
                          Example: `func:test__basic_model__init_on_access_flag`
        """
        # seems like it is default
        self.value = value
        self._help = help
        self._required = required
        self.default = default
        self._on_access = on_access

    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, instance, owner):
        # support iterate over class fields
        if instance is None:
            return owner.__dict__.get(self._name)
        # support iterate over instance fields
        if self._name in dir(owner):
            v = instance.get(self._name, None)
            if v:
                pass
            elif self._on_access is True:
                v_type = instance.__annotations__.get(self._name, None)
                if v_type is None:
                    raise ValueError("on_access=True without type annotation")
                elif 'typing.List' in str(v_type):
                    v = []
                elif 'typing.Dict' in str(v_type):
                    v = {}
                else:
                    v = v_type()
                instance[self._name] = v
            elif self._on_access:
                # TODO: lock for raise condition?
                v = self._on_access()
                instance[self._name] = v
            return v
        raise ValueError(self._name)

    def __set__(self, instance, value):
        instance[self._name] = value


Field = DictField


class BaseModelMeta(type):
    def __new__(mcs, name, bases, attrs):
        cls = super(BaseModelMeta, mcs).__new__(mcs, name, bases, attrs)
        for attr, obj in attrs.items():
            if isinstance(obj, DictField):
                obj.__set_name__(cls, attr)
        return cls


# --- trick to stop intellisence ---
def _get_base() -> type:
    return dict


_ModelBase = _get_base()


# --- trick to stop intellisence ---

class ModelBase(_ModelBase):

    def _update_default_values_on_fields(self):
        """ Instantiate default values
        """
        for k in self.__class__.get_all_keys(only_smart=True):
            # update default values on fields
            if self.get(k, None) is None:
                att: DictField = getattr(self.__class__, k)
                if att.value is not None:
                    self[k] = att.value
                # default factory create if callable
                elif att.default is not None:
                    if callable(att.default):
                        self[k] = att.default()
                    else:
                        self[k] = att.default

            # TODO: change to preprocessing
            elif hasattr(self, '__annotations__') and k in self.__annotations__:
                v_type = self.__annotations__[k]
                if isinstance(v_type, type) and issubclass(
                    v_type, (str, int, bool, float)):
                    # do not create immutable primitives save time and memory
                    # self[k] = v_type(self[k])
                    pass
                elif isinstance(v_type, type) and issubclass(v_type, list):
                    self[k] = list(self[k])
                elif isinstance(v_type, type) and v_type is dict:
                    self[k] = dict(self[k])
                elif 'typing.List[typing.List' in str(v_type):
                    # currently no can do list of lists
                    logging.warning("cannot instantiate List[List[T]]")
                elif 'typing.List' in str(v_type):
                    # treat List from typing
                    types = get_subtypes(v_type)
                    if len(types) > 1:
                        logging.warning(f"Too many types for list {types} using first")
                    the_type = types[0]
                    # HACK untill data type valid
                    try:
                        v_typed = [the_type(val) for val in self[k]]
                        self[k] = v_typed
                    except TypeError as ex:
                        logging.error(f"Failed to instantiate {the_type} on {k}")
                elif 'typing.Dict' in str(v_type):
                    # treat Dict from typing 
                    types = get_subtypes(v_type)
                    if len(types) > 2:
                        logging.warning(f"Too many types for list {types} using first")
                    the_type, bt = types
                    # HACK untill data type valid
                    try:
                        v_typed = { the_type(_k): bt(_v) for _k, _v in self[k].items() }
                        self[k] = v_typed
                    except TypeError as ex:
                        logging.error(f"Failed to instantiate {the_type} on {k}")
                elif isinstance(v_type, type) and issubclass(v_type, (DictModel, dict,)):
                    # treat a regular dict
                    try:
                         self[k] = v_type(**self[k])
                    except TypeError:
                        import traceback
                        traceback.print_exc()
                        logging.error(f"k={k} ")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._update_default_values_on_fields()

    @classmethod
    def get_all_keys(cls, only_smart=False) -> List[str]:
        """ Returns: all well known keys () defined in model
        :param only_smart: if True - only keys defiend with DictField
        :return: keys in object that is not callable and not hidden
        """
        keys = [
            f for f in dir(cls)
            if not callable(getattr(cls, f)) and not f.startswith('__')
        ]
        if only_smart:
            keys = [it for it in keys if isinstance(getattr(cls, it), DictField)]
        return keys

    @classmethod
    def get_all_vals(cls, only_smart=False) -> list:
        """ Returns: all well known keys () defined in model
        :param only_smart: if True - only keys defiend with DictField
        :return: keys in object that is not callable and not hidden
        """
        vals = [getattr(cls, name) for name in cls.get_all_keys(only_smart=only_smart)]
        return vals

    def to_yaml_str(self):
        """Returns yaml representation of the object
        """
        import io
        sio = io.StringIO()
        yaml.dump(dict(self.to_struct()), sio)
        s = sio.getvalue()
        return s

    def to_yaml(self, filepath):
        with Path(filepath).open('w') as fp:
            yaml.dump(self.to_struct(), fp)

    @classmethod
    def from_yaml(cls, filepath):
        with Path(filepath).open('r') as fp:
            return cls(yaml.load(fp))

    def to_json(self, filepath):
        with Path(filepath).open('w') as fp:
            json.dump(self, fp, indent=2, sort_keys=True)

    def to_json_str(self, one_line=False) -> str:
        """ Converts object to json string
        :param one_line: if True will format in one line
        :return: string with json representation of object with sorted keys
        """
        if one_line:
            ps = dict(sort_keys=True)
        else:
            ps = dict(indent=2, sort_keys=True)
        return json.dumps(self, **ps)

    @classmethod
    def from_json(cls, filepath):
        with Path(filepath).open('r') as fp:
            return cls(json.load(fp))

    def to_struct(self):
        return to_struct(self)

    @classmethod
    def from_struct(cls, struct):
        return cls(struct)

    @classmethod
    def from_path(cls, path):
        if path.endswith('yml') or path.endswith('yaml'):
            return cls.from_yaml(path)
        elif path.endswith('json'):
            return cls.from_json(path)
        else:
            raise Exception('path is not supported: {}'
                            '(only json and yaml)'.format(path))

    def to_path(self, path):
        if path.endswith('yml') or path.endswith('yaml'):
            return self.to_yaml(path)
        elif path.endswith('json'):
            return self.to_json(path)
        else:
            raise Exception('path is not supported: {}'
                            '(only json and yaml)'.format(path))

    @classmethod
    def from_flask(cls, flask_request):
        print('sdf')
        import json
        struct = json.loads(flask_request.get_data().decode())
        # struct = flask_request.get_json()
        return cls(struct)


def to_struct(x):
    from contextlib import suppress
    
    # support non-required libraries
    with suppress(ImportError):
        from jsonmodels import models
        if isinstance(x, models.Base):
            return x.to_struct()
    
    # hopefully we all mead python hierachical dict/list structure
    if isinstance(x, (DictModel, dict)):
        return {k: to_struct(v) for k, v in x.items()}
    elif isinstance(x, list):
        return [to_struct(it) for it in x]
    if hasattr(x, 'to_struct'):
        return x.to_struct()
    else:
        return x

def to_file(x, filepath):
    if hasattr(x, 'to_file'):
        return x.to_file(filepath)
    elif any(filepath.endswith(ext) for ext in ['.yaml', '.yml']):
        with Path(filepath).open('w') as fp:
            yaml.dump(to_struct(x), fp)
    elif any(filepath.endswith(ext) for ext in ['.json', '.ndjson']):
        with Path(filepath).open('w') as fp:
            json.dump(to_struct(x), fp)
    else:
        raise ValueError(f"Unsupported {filepath} for {x}")
DictModel = ModelBase
