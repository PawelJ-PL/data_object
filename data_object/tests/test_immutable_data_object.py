from json import JSONEncoder
from unittest import TestCase

from datetime import datetime

from data_object import ImmutableDataObject
from data_object.exceptions import ImmutableObjectViolation


class TestImmutableDataObject(TestCase):
    def test_should_create_immutable_data_object(self):
        # given
        class SimpleClass(ImmutableDataObject):
            def __init__(self, foo, bar):
                self.foo = foo
                self.bar = bar

        # when
        instance = SimpleClass('x', 'y')

        # then
        self.assertEqual(instance.__str__(), '{"bar": "y", "foo": "x"}')

    def test_should_raise_exception_on_changing_attribute(self):
        # given
        class SimpleClass(ImmutableDataObject):
            def __init__(self, foo, bar):
                self.foo = foo
                self.bar = bar

        instance = SimpleClass('x', 'y')

        # when
        with self.assertRaisesRegex(ImmutableObjectViolation, 'Changing attributes not permitted for immutable object'):
            instance.bar = 'abc'

    def test_should_user_custom_json_encoder(self):
        # given
        class SimpleClass(ImmutableDataObject):
            _json_encoder = JSONEncoder

            def __init__(self, foo, bar):
                self.foo = foo
                self.bar = bar

        # when
        instance = SimpleClass('x', datetime(2000, 10, 5, 14, 30))

        # then
        with self.assertRaisesRegex(TypeError, 'datetime.datetime\(2000, 10, 5, 14, 30\) is not JSON serializable'):
            self.assertEqual(instance.__str__(), '{"bar": "y", "foo": "x"}')

    def test_should_copy_instance_with_new_value(self):
        # given
        class SimpleClass(ImmutableDataObject):
            def __init__(self, foo, bar):
                self.foo = foo
                self.bar = bar

        instance = SimpleClass('x', 'y')

        # when
        result = instance.copy(bar='abc')

        # then
        self.assertEqual(result.foo, 'x')
        self.assertEqual(result.bar, 'abc')
