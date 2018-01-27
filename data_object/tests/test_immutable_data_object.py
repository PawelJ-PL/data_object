from unittest import TestCase

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
        self.assertEqual('SimpleClass: {"bar": y, "foo": x}', instance.__str__(), )

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
