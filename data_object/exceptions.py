class DataObjectException(Exception):
    pass


class ConstructorKeywordArgumentNotFound(DataObjectException):
    def __init__(self, kwarg) -> None:
        super().__init__('Constructor argument {} not found'.format(kwarg))


class ImmutableObjectViolation(DataObjectException):
    pass
