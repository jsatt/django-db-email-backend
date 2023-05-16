#!/usr/bin/env python

import os
import sys

from distutils.core import setup

import db_email_backend

if sys.argv[-1] == 'publish':
    os.system("python setup.py sdist upload")
    sys.exit()

# long_description = open('README.md').read_text()
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.rst").read_text()

setup(
    name='kn-django-db-email-backend',
    version=db_email_backend.__version__,
    description='Django email backend for storing messages to a database.',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    author='Ramez Ashraf',
    author_email='ramez@kuwaitnet.com',
    url='https://github.com/KUWAITNET/django-db-email-backend',
    license="MIT License",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development',
    ],
    packages=[
        'db_email_backend',
        'db_email_backend.migrations',
    ],
    install_requires=[
        "django>=2.2",
        "pytz",
    ],
)
