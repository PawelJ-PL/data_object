from abc import ABCMeta
from functools import reduce
from inspect import getfullargspec, signature, _empty

from copy import deepcopy

from data_object.exceptions import ConstructorKeywordArgumentNotFound, ImmutableObjectViolation


class DataObject(metaclass=ABCMeta):

    def as_json(self):
        return {key: value for key, value in self.__dict__.items() if not key.startswith('_')}

    @classmethod
    def from_dict(cls, params: dict, none_if_not_found=False):
        constructor_args = deepcopy(getfullargspec(cls.__init__).args)
        del constructor_args[0]
        kwargs = {}
        for arg in constructor_args:
            try:
                kwargs[arg] = params[arg]
            except KeyError as err:
                default_val = signature(cls.__init__).parameters.get(arg).default
                if default_val is not _empty:
                    kwargs[arg] = default_val
                elif none_if_not_found:
                    kwargs[arg] = None
                else:
                    raise ConstructorKeywordArgumentNotFound(err)
        # noinspection PyArgumentList
        return cls(**kwargs)

    def copy(self, **attributes):
        attrs = {**self.as_json(), **attributes}
        return type(self).from_dict(attrs)

    def __str__(self) -> str:
        attr_values = self.as_json()
        attr_names = sorted(attr_values.keys())
        pairs = ['"{0}": {1}'.format(attr, attr_values[attr]) for attr in attr_names]
        return '{0}: {{{1}}}'.format(self.__class__.__name__, ', '.join(pairs))

    def __repr__(self) -> str:
        attr_values = self.as_json()
        attr_names = sorted(attr_values.keys())
        pairs = ['{0}={1}'.format(attr, attr_values[attr]) for attr in attr_names]
        return '{0}({1})'.format(self.__class__.__name__, ', '.join(pairs))

    def __eq__(self, o: object) -> bool:
        if not hasattr(o, 'as_json'):
            return False
        return self.as_json() == o.as_json()

    def __ne__(self, o: object) -> bool:
        return not self.__eq__(o)

    def __hash__(self) -> int:
        attr_values = sorted("{0}:{1}".format(key, value) for key, value in self.as_json().items())
        hashes = reduce(lambda prev_attr, next_attr: hash(prev_attr) ^ hash(next_attr), attr_values, 0)
        return hashes


class ImmutableDataObject(DataObject):

    def __setattr__(self, name: str, value) -> None:
        try:
            getattr(self, name)
        except AttributeError:
            super().__setattr__(name, value)
            return
        raise ImmutableObjectViolation('Changing attributes not permitted for immutable object')
