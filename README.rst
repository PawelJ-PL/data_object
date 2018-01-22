data\_object
============

Description:
------------

Simple base class for creating data object (it means objects, dedicated
to storing data only). It's a little bit similar to `case
class <https://docs.scala-lang.org/tour/case-classes.html>`__ from
Scala. Using it as base class, You don't need to take care of data
objects boilerplate (like \_\_str\_\_, \_\_eq\_\_, \_\_hash\_\_
methods). Main features: \* Objects are considered to be equal based on
public fields (method with names started with \_ are not took into
account) values instead of object identity \* \_\_str\_\_ and
\_\_repr\_\_ methods return values based on public fields \* Static
method for creating instances from dictionary. Main difference to dict
unpacking is that all non matching keys are ignored and default values
are supported \* there are two base classes: **DataObject** and
**ImmutableDataObject**. The second on creates immutable object (so
value assigned once to field, cannot be changed)

**WARNING:** > In future version default behavior may change. It's still
under consideration, whether two different classes with the same set of
fields and values should be equal

Install
-------

``pip install data_object``

Usage
-----

DataObject
^^^^^^^^^^

.. code:: python

    from data_object import DataObject


    class CustomClass(DataObject):
        def __init__(self, foo, bar):
            self.foo = foo
            self.bar = bar

Str and Repr:
             

.. code:: python

    a = CustomClass('a', 'b')
    print(a) # output: {"bar": "b", "foo": "a"}
    print(repr(a)) # output: CustomClass(bar=b, foo=a)

Equality and Hash
                 

.. code:: python


    class OtherClass(DataObject):
        def __init__(self, foo, bar):
            self.foo = foo
            self.bar = bar

    a = CustomClass('a', 'b')
    b = CustomClass('a', 'b')
    c = CustomClass('a', 'z')
    d = OtherClass('a', 'b')

    a == b # True
    a == c # False
    a == d # True

    z = set()
    z.add(a)
    z.add(b)
    z.add(c)
    z.add(d)
    print(z) # output: {CustomClass(bar=b, foo=a), CustomClass(bar=z, foo=a)}

Creating instances from dict
                            

.. code:: python

    class SomeClass(DataObject):
        def __init__(self, a, b, c='xyz'):
            self.a = a
            self.b = b
            self.c = c

    params1 = {'a': 'aaa', 'b': 'bbb', 'c': 'ccc'}
    params2 = {'a': 'xxx', 'b': 'yyy'}
    params3 = {'a': 'xxx'}

    inst1 = SomeClass.from_dict(params1)
    inst2 = SomeClass.from_dict(params2)
    inst3 = SomeClass.from_dict(params3, none_if_not_found=True)

    print(inst1) # output: {"a": "aaa", "b": "bbb", "c": "ccc"}
    print(inst2) # output: {"a": "xxx", "b": "yyy", "c": "xyz"}
    print(inst3) # output: {"a": "xxx", "b": null, "c": "xyz"}

ImmutableDataObject
^^^^^^^^^^^^^^^^^^^

.. code:: python

    from data_object import ImmutableDataObject

    class CustomImmutableClass(ImmutableDataObject):
        def __init__(self, foo, bar):
            self.foo = foo
            self.bar = bar

    inst = CustomImmutableClass('abc', 'xyz')
    print(inst) # output: {"bar": "xyz", "foo": "abc"}

    inst.foo = 'aaa'

will produce exception:

::

    Traceback (most recent call last):
    ...
    data_object.exceptions.ImmutableObjectViolation: Changing attributes not permitted for immutable object
