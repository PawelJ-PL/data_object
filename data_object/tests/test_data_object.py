from datetime import datetime
from enum import Enum
from unittest import TestCase

from data_object import DataObject
from data_object.exceptions import ConstructorKeywordArgumentNotFound


class TestDataObject(TestCase):

    def test_should_create_data_object_and_get_as_string(self):
        # given
        class SimpleClass(DataObject):
            def __init__(self, foo, bar):
                self.foo = foo
                self.bar = bar

        # when
        instance = SimpleClass('x', 'y')

        # then
        self.assertEqual('SimpleClass: {"bar": y, "foo": x}', instance.__str__())

    def test_should_create_data_object_with_datetime_and_get_as_string(self):
        # given
        class SimpleClass(DataObject):
            def __init__(self, foo, bar):
                self.foo = foo
                self.bar = bar

        # when
        instance = SimpleClass('x', datetime(2000, 10, 5, 14, 30))

        # then
        self.assertEqual('SimpleClass: {"bar": 2000-10-05 14:30:00, "foo": x}', instance.__str__())

    def test_should_create_data_object_with_enum_and_get_as_string(self):
        # given
        class SomeEnum(Enum):
            VAL1 = 'val1'

        class SimpleClass(DataObject):
            def __init__(self, foo, bar):
                self.foo = foo
                self.bar = bar

        # when
        instance = SimpleClass('x', SomeEnum.VAL1)

        # then
        self.assertEqual('SimpleClass: {"bar": SomeEnum.VAL1, "foo": x}', instance.__str__())

    def test_should_create_child_data_object_and_get_as_string(self):
        # given
        class SimpleClass(DataObject):
            def __init__(self, foo, bar):
                self.foo = foo
                self.bar = bar

        class ChildClass(SimpleClass):

            def __init__(self, foo, bar, other):
                super().__init__(foo, bar)
                self.other = other

        # when
        instance = ChildClass('x', 'y', 'z')

        # then
        self.assertEqual('ChildClass: {"bar": y, "foo": x, "other": z}', instance.__str__())

    def test_should_create_data_object_with_method_and_get_as_string(self):
        # given
        class SimpleClass(DataObject):
            def __init__(self, foo, bar):
                self.foo = foo
                self.bar = bar

            def some_method(self, x):
                return self.foo * x

        # when
        instance = SimpleClass('x', 'y')

        # then
        self.assertEqual('SimpleClass: {"bar": y, "foo": x}', instance.__str__())

    def test_should_create_data_object_with_protected_field_and_get_as_string(self):
        # given
        class SimpleClass(DataObject):
            def __init__(self, foo, bar):
                self.foo = foo
                self.bar = bar
                self._other = foo + bar

        # when
        instance = SimpleClass('x', 'y')

        # then
        self.assertEqual('SimpleClass: {"bar": y, "foo": x}', instance.__str__())

    def test_should_create_data_object_and_get_repr(self):
        # given
        class SimpleClass(DataObject):
            def __init__(self, foo, bar):
                self.foo = foo
                self.bar = bar

        # when
        instance = SimpleClass('x', 'y')

        # then
        self.assertEqual(instance.__repr__(), 'SimpleClass(bar=y, foo=x)')

    def test_should_return_equal_true_for_object_with_same_fields(self):
        # given
        class SimpleClass(DataObject):
            def __init__(self, foo, bar):
                self.foo = foo
                self.bar = bar

        # when
        instance1 = SimpleClass('x', 'y')
        instance2 = SimpleClass(bar='y', foo='x')

        # then
        self.assertEqual(instance1, instance2)

    def test_should_return_equal_false_for_object_with_different_fields(self):
        # given
        class SimpleClass(DataObject):
            def __init__(self, foo, bar):
                self.foo = foo
                self.bar = bar

        # when
        instance1 = SimpleClass('x', 'y')
        instance2 = SimpleClass(bar='z', foo='x')

        # then
        self.assertNotEqual(instance1, instance2)

    def test_should_return_equal_true_for_object_with_same_fields_and_no_subclass(self):
        # given
        class SimpleClass(DataObject):
            def __init__(self, foo, bar):
                self.foo = foo
                self.bar = bar

        class OtherClass(DataObject):
            def __init__(self, foo, bar):
                self.foo = foo
                self.bar = bar

        # when
        instance1 = SimpleClass('x', 'y')
        instance2 = OtherClass('x', 'y')

        # then
        self.assertEqual(instance1, instance2)

    def test_should_return_equal_true_for_object_with_same_fields_and_subclass(self):
        # given
        class SimpleClass(DataObject):
            def __init__(self, foo, bar):
                self.foo = foo
                self.bar = bar

        class OtherClass(SimpleClass):
            pass

        # when
        instance1 = SimpleClass('x', 'y')
        instance2 = OtherClass('x', 'y')

        # then
        self.assertEqual(instance1, instance2)

    def test_should_return_equal_true_for_object_with_same_fields_and_subclass_changed_order(self):
        # given
        class SimpleClass(DataObject):
            def __init__(self, foo, bar):
                self.foo = foo
                self.bar = bar

        class OtherClass(SimpleClass):
            pass

        # when
        instance1 = SimpleClass('x', 'y')
        instance2 = OtherClass('x', 'y')

        # then
        self.assertEqual(instance2, instance1)

    def test_should_return_equal_true_for_object_with_same_fields_and_subclass_changed_hierarchy(self):
        # given
        class OtherClass(DataObject):
            def __init__(self, foo, bar):
                self.foo = foo
                self.bar = bar

        class SimpleClass(OtherClass):
            pass

        # when
        instance1 = SimpleClass('x', 'y')
        instance2 = OtherClass('x', 'y')

        # then
        self.assertEqual(instance1, instance2)

    def test_should_return_equal_true_for_object_with_same_fields_and_no_subclass_changed_order(self):
        # given
        class SimpleClass(DataObject):
            def __init__(self, foo, bar):
                self.foo = foo
                self.bar = bar

        class OtherClass(DataObject):
            def __init__(self, foo, bar):
                self.foo = foo
                self.bar = bar

        # when
        instance1 = SimpleClass('x', 'y')
        instance2 = OtherClass('x', 'y')

        # then
        self.assertEqual(instance2, instance1)

    def test_should_raise_exception_on_equal_if_no_to_json_method(self):
        # given
        class SimpleClass(DataObject):
            def __init__(self, foo, bar):
                self.foo = foo
                self.bar = bar

        class OtherClass:
            def __init__(self, foo, bar):
                self.foo = foo
                self.bar = bar

        instance1 = SimpleClass('x', 'y')
        instance2 = OtherClass('x', 'y')

        # then
        self.assertNotEqual(instance1, instance2)

    def test_should_not_add_equal_values_to_set_twice_for_the_same_class(self):
        # given
        class SimpleClass(DataObject):
            def __init__(self, foo, bar):
                self.foo = foo
                self.bar = bar

        result = set()

        # when
        instance1 = SimpleClass('x', 'y')
        instance2 = SimpleClass(bar='y', foo='x')
        result.add(instance1)
        result.add(instance2)

        # then
        self.assertEqual(len(result), 1)

    def test_should_not_add_equal_values_to_set_twice_when_subclass(self):
        # given
        class SimpleClass(DataObject):
            def __init__(self, foo, bar):
                self.foo = foo
                self.bar = bar

        class OtherClass(SimpleClass):
            pass

        result = set()

        # when
        instance1 = SimpleClass('x', 'y')
        instance2 = OtherClass(bar='y', foo='x')
        result.add(instance1)
        result.add(instance2)

        # then
        self.assertEqual(len(result), 1)

    def test_should_not_add_equal_values_to_set_twice_when_no_subclass(self):
        # given
        class SimpleClass(DataObject):
            def __init__(self, foo, bar):
                self.foo = foo
                self.bar = bar

        class OtherClass(DataObject):
            def __init__(self, foo, bar):
                self.foo = foo
                self.bar = bar

        result = set()

        # when
        instance1 = SimpleClass('x', 'y')
        instance2 = OtherClass(bar='y', foo='x')
        result.add(instance1)
        result.add(instance2)

        # then
        self.assertEqual(len(result), 1)

    def test_should_add_different_values_to_set(self):
        # given
        class SimpleClass(DataObject):
            def __init__(self, foo, bar):
                self.foo = foo
                self.bar = bar

        result = set()

        # when
        instance1 = SimpleClass('x', 'y')
        instance2 = SimpleClass(bar='z', foo='x')
        result.add(instance1)
        result.add(instance2)

        # then
        self.assertEqual(len(result), 2)

    def test_should_create_instance_from_dict(self):
        # given
        class SimpleClass(DataObject):
            def __init__(self, foo, bar):
                self.foo = foo
                self.bar = bar

        data = {'bar': 'y', 'foo': 'x'}

        # when
        instance = SimpleClass.from_dict(data)

        # then
        self.assertIsInstance(instance, SimpleClass)
        self.assertEqual(instance.foo, 'x')
        self.assertEqual(instance.bar, 'y')

    def test_should_raise_exception_when_constructor_arg_not_found(self):
        # given
        class SimpleClass(DataObject):
            def __init__(self, foo, bar):
                self.foo = foo
                self.bar = bar

        data = {'bar': 'y'}

        # when
        with self.assertRaisesRegex(ConstructorKeywordArgumentNotFound, "Constructor argument 'foo' not found"):
            SimpleClass.from_dict(data)

    def test_should_set_arg_with_none_when_value_not_found(self):
        # given
        class SimpleClass(DataObject):
            def __init__(self, foo, bar):
                self.foo = foo
                self.bar = bar

        data = {'bar': 'y'}

        # when
        instance = SimpleClass.from_dict(data, none_if_not_found=True)

        # then
        self.assertIsInstance(instance, SimpleClass)
        self.assertIsNone(instance.foo)
        self.assertEqual(instance.bar, 'y')

    def test_should_create_instance_from_dict_with_defaults_in_constructor_and_all_provided(self):
        # given
        class SimpleClass(DataObject):
            def __init__(self, foo, bar='xyz'):
                self.foo = foo
                self.bar = bar

        data = {'bar': 'y', 'foo': 'x'}

        # when
        instance = SimpleClass.from_dict(data)

        # then
        self.assertIsInstance(instance, SimpleClass)
        self.assertEqual(instance.foo, 'x')
        self.assertEqual(instance.bar, 'y')

    def test_should_create_instance_from_dict_with_defaults_in_constructor_and_not_all_provided(self):
        # given
        class SimpleClass(DataObject):
            def __init__(self, foo, bar='xyz'):
                self.foo = foo
                self.bar = bar

        data = {'foo': 'x'}

        # when
        instance = SimpleClass.from_dict(data)

        # then
        self.assertIsInstance(instance, SimpleClass)
        self.assertEqual(instance.foo, 'x')
        self.assertEqual(instance.bar, 'xyz')

    def test_should_create_instance_from_dict_when_more_args_provided(self):
        # given
        class SimpleClass(DataObject):
            def __init__(self, foo, bar):
                self.foo = foo
                self.bar = bar

        data = {'bar': 'y', 'foo': 'x', 'other': 'xyz'}

        # when
        instance = SimpleClass.from_dict(data)

        # then
        self.assertIsInstance(instance, SimpleClass)
        self.assertEqual('SimpleClass: {"bar": y, "foo": x}', instance.__str__())

    def test_should_create_data_object_and_get_as_string_when_self_renamed(self):
        # given
        class SimpleClass(DataObject):
            # noinspection PyMethodParameters
            def __init__(other, foo, bar):
                other.foo = foo
                other.bar = bar

        # when
        instance = SimpleClass('x', 'y')

        # then
        self.assertEqual('SimpleClass: {"bar": y, "foo": x}', instance.__str__())

    def test_should_copy_instance(self):
        # given
        class SimpleClass(DataObject):
            def __init__(self, foo, bar):
                self.foo = foo
                self.bar = bar

        inst1 = SimpleClass('abc', 'xyz')

        # when
        inst2 = inst1.copy()

        # then
        self.assertIsInstance(inst2, SimpleClass)
        self.assertEqual(inst1, inst2)

    def test_should_copy_instance_with_all_changed_fields(self):
        # given
        class SimpleClass(DataObject):
            def __init__(self, foo, bar):
                self.foo = foo
                self.bar = bar

        inst1 = SimpleClass('abc', 'xyz')

        # when
        inst2 = inst1.copy(foo='aa', bar='bb')

        # then
        self.assertIsInstance(inst2, SimpleClass)
        self.assertEqual('SimpleClass: {"bar": bb, "foo": aa}', str(inst2))

    def test_should_copy_instance_with_some_changed_fields(self):
        # given
        class SimpleClass(DataObject):
            def __init__(self, foo, bar):
                self.foo = foo
                self.bar = bar

        inst1 = SimpleClass('abc', 'xyz')

        # when
        inst2 = inst1.copy(foo='aa')

        # then
        self.assertIsInstance(inst2, SimpleClass)
        self.assertEqual(str(inst2), 'SimpleClass: {"bar": xyz, "foo": aa}')

    def test_should_copy_instance_with_not_known_field_fields(self):
        # given
        class SimpleClass(DataObject):
            def __init__(self, foo, bar):
                self.foo = foo
                self.bar = bar

        inst1 = SimpleClass('abc', 'xyz')

        # when
        inst2 = inst1.copy(foo='aa', zz='cc')

        # then
        self.assertIsInstance(inst2, SimpleClass)
        self.assertEqual(str(inst2), 'SimpleClass: {"bar": xyz, "foo": aa}')
        self.assertFalse(hasattr(inst2, 'zz'))
