#! /usr/bin/env python

from setuptools import setup

setup(name="django-dont-vary-on",
      version="1.0.0",
      author="Rory McCann",
      author_email="rory@technomancy.org",
      packages=['django_dont_vary_on'],
      license = 'GPLv3',
      description = "Library for Django to give you more control over Django's caching, and improving you cache hits and performance",
      install_requires = [ 'django' ],
)
