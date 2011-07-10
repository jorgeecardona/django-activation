from setuptools import setup, find_packages
from os.path import join, abspath, dirname

fd = open(join(abspath(dirname(__file__)), 'README.rst'))
long_description = fd.read()
fd.close()

setup(
    name='django-activation',
    description='Simple activation of users.',
    long_description=long_description,
    version='0.1.0b',
    author='Jorge Eduardo Cardona Gaviria',
    author_email='jorgeecardona@gmail.com',
    packages=find_packages(),
    install_requires=[
        'django',
        ])
