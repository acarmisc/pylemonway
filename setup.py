from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pylemonway',
    version='0.1.1',
    description='Python wrapper for Lemonway DIRECTKITJSON2',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/acarmisc/pylemonway',

    # Author details
    author='Andrea Carmisciano',
    author_email='andrea.carmisciano@gmail.com',

    license='APACHE 2.0',
    classifiers=[
        'Development Status :: 4 - Beta',
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='REST lemonway requests crowdfunding',

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['requests'],
)
