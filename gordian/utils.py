from typing import TypeVar, Dict, Tuple, Mapping, Generic

_KT = TypeVar('_KT')
_VT = TypeVar('_VT')


class ReversibleDict(Dict[_KT, _VT]):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._inv = dict()
        for k, v in self.items():
            self._inv[v] = self._inv.get(v, set()).union({k})

    @property
    def inv(self):
        return ImmutableDict(self._inv)

    def __setitem__(self, key: _KT, value: _VT):
        if key in self:
            self.__delitem__(key)
        super().__setitem__(key, value)
        self._inv[value] = self._inv.get(value, set()).union({key})

    def __delitem__(self, key: _KT):
        v = self[key]
        self._inv[v].remove(key)
        if len(self._inv[v]) == 0:
            self._inv.__delitem__(v)
        super().__delitem__(key)

    def clear(self) -> None:
        super().clear()
        self._inv.clear()

    def pop(self, key: _KT) -> _VT:
        v = self[key]
        self.__delitem__(key)
        return v

    def popitem(self) -> Tuple[_KT, _VT]:
        last_key = list(self.keys())[-1]
        return last_key, self.pop(last_key)

    def update(self, __m: Mapping[_KT, _VT]=None, **kwargs: _VT) -> None:
        if __m is None:
            __m = dict(**kwargs)
        for k, v in __m.items():
            self.__setitem__(k, v)

    def setdefault(self, __key: _KT, __default: _VT = ...) -> _VT:
        if __key in self:
            return self[__key]
        self.__setitem__(__key, __default)
        return __default


class ImmutableDict(dict):
    def __hash__(self):
        return id(self)

    def _immutable(self, *args, **kws):
        raise TypeError('object is immutable')

    __setitem__ = _immutable
    __delitem__ = _immutable
    clear       = _immutable
    update      = _immutable
    setdefault  = _immutable
    pop         = _immutable
    popitem     = _immutable