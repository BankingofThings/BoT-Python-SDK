from io import open

from setuptools import find_packages, setup

with open('bot_python_sdk/__init__.py', 'r') as f:
    for line in f:
        if line.startswith('__version__'):
            version = line.strip().split('=')[1].strip(' \'"')
            break
    else:
        version = '0.0.1'

with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()

REQUIRES = []

setup(
    name='BoT-Python-SDK',
    license='Apache-2.0',
    version=version,
    description='',
    long_description=readme,
    author='Banking of Things',
    author_email='bankingofthings@ing.nl',
    maintainer='Banking of Things',
    maintainer_email='bankingofthings@ing.nl',
    url='https://github.com/BankingofThings/BoT-Python-SDK',

    keywords=[
        '',
    ],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],

    install_requires=REQUIRES,
    tests_require=['coverage', 'pytest'],

    packages=find_packages(),
)
