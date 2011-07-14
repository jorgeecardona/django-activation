from setuptools import setup, find_packages
from os.path import join, abspath, dirname
from random import choice
from string import lowercase


def read_file(name):
    fd = open(join(abspath(dirname(__file__)), name))
    data = fd.read()
    fd.close()
    return data

setup(
    name='django-activation',
    description='Simple activation of users.',
    long_description=read_file('README.rst'),
    version='0.1.2%s' % (choice(lowercase), ),
    author='Jorge Eduardo Cardona Gaviria',
    author_email='jorgeecardona@gmail.com',
    packages=find_packages(),
    install_requires=[
        'django',
        ])
