"""
Fixes for typing module that have differences in py3.6 py3.7
https://stackoverflow.com/questions/48572831/how-to-access-the-type-arguments-of-typing-generic
https://stackoverflow.com/questions/49171189/whats-the-correct-way-to-check-if-an-object-is-a-typing-generic

"""
import typing


if hasattr(typing, '_GenericAlias'):
    # python 3.7
    def _get_base_generic(cls):
        # subclasses of Generic will have their _name set to None, but
        # their __origin__ will point to the base generic
        if cls._name is None:
            return cls.__origin__
        else:
            return getattr(typing, cls._name)

    # python 3.7
    def _is_generic(cls):
        if isinstance(cls, typing._GenericAlias):
            return True

        if isinstance(cls, typing._SpecialForm):
            return cls not in {typing.Any}

        return False


    def _is_base_generic(cls):
        if isinstance(cls, typing._GenericAlias):
            if cls.__origin__ in {typing.Generic, typing._Protocol}:
                return False

            if isinstance(cls, typing._VariadicGenericAlias):
                return True

            return len(cls.__parameters__) > 0

        if isinstance(cls, typing._SpecialForm):
            return cls._name in {'ClassVar', 'Union', 'Optional'}

        return False
else:
    # python <3.7
    def _get_base_generic(cls):
        try:
            return cls.__origin__
        except AttributeError:
            pass

        name = type(cls).__name__
        if not name.endswith('Meta'):
            raise NotImplementedError("Cannot determine base of {}".format(cls))

        name = name[:-4]
        try:
            return getattr(typing, name)
        except AttributeError:
            raise NotImplementedError("Cannot determine base of {}".format(cls))

    # python <3.7
    if hasattr(typing, '_Union'):
        # python 3.6
        def _is_generic(cls):
            if isinstance(cls, (typing.GenericMeta, typing._Union, typing._Optional, typing._ClassVar)):
                return True

            return False


        def _is_base_generic(cls):
            if isinstance(cls, (typing.GenericMeta, typing._Union)):
                return cls.__args__ in {None, ()}

            if isinstance(cls, typing._Optional):
                return True

            return False
    else:
        # python 3.5
        def _is_generic(cls):
            if isinstance(cls, (typing.GenericMeta, typing.UnionMeta, typing.OptionalMeta, typing.CallableMeta, typing.TupleMeta)):
                return True

            return False


        def _is_base_generic(cls):
            if isinstance(cls, typing.GenericMeta):
                return all(isinstance(arg, typing.TypeVar) for arg in cls.__parameters__)

            if isinstance(cls, typing.UnionMeta):
                return cls.__union_params__ is None

            if isinstance(cls, typing.TupleMeta):
                return cls.__tuple_params__ is None

            if isinstance(cls, typing.CallableMeta):
                return cls.__args__ is None

            if isinstance(cls, typing.OptionalMeta):
                return True

            return False

if hasattr(typing.List, '__args__'):
    # python 3.6+
    def _get_subtypes(cls):
        subtypes = cls.__args__

        if _get_base_generic(cls) is typing.Callable:
            if len(subtypes) != 2 or subtypes[0] is not ...:
                subtypes = (subtypes[:-1], subtypes[-1])

        return subtypes
else:
    # python 3.5
    def _get_subtypes(cls):
        if isinstance(cls, typing.CallableMeta):
            if cls.__args__ is None:
                return ()

            return cls.__args__, cls.__result__

        for name in ['__parameters__', '__union_params__', '__tuple_params__']:
            try:
                subtypes = getattr(cls, name)
                break
            except AttributeError:
                pass
        else:
            raise NotImplementedError("Cannot extract subtypes from {}".format(cls))

        subtypes = [typ for typ in subtypes if not isinstance(typ, typing.TypeVar)]
        return subtypes


def get_subtypes(cls):
    """
    Given a qualified generic (like List[int] or Tuple[str, bool]) as input, return
    a tuple of all the classes listed inside the square brackets.
    """
    return _get_subtypes(cls)


def is_generic(cls):
    """
    Detects any kind of generic, for example `List` or `List[int]`. This includes "special" types like
    Union and Tuple - anything that's subscriptable, basically.
    """
    return _is_generic(cls)


def is_base_generic(cls):
    """
    Detects generic base classes, for example `List` (but not `List[int]`)
    """
    return _is_base_generic(cls)


def is_qualified_generic(cls):
    """
    Detects generics with arguments, for example `List[int]` (but not `List`)
    """
    return is_generic(cls) and not is_base_generic(cls)
