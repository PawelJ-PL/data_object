from os import path
from setuptools import setup, find_packages


here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst')) as f:
    long_description = f.read()


setup(
    name='data_object',
    use_scm_version=True,
    description='Base class for data objects',
    long_description=long_description,
    url='https://github.com/PawelJ-PL/data_object',
    author='Pawel',
    author_email='inne.poczta@gmail.com',
    maintainer='Pawel',
    maintainer_email='inne.poczta@gmail.com',
    license='MIT',
    keywords='Python data object case class boilerplate dto',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries'
    ],
    packages=find_packages(),
    extras_require={
        'test': ['coverage', 'nose'],
    },
    tests_require=['nose', 'coverage'],
    setup_requires=['setuptools_scm', 'wheel'],
    python_requires='>=3',
    test_suite='nose.collector',
)
