# !/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='django-admin-history-detail',
    version='0.1.0',
    url='https://github.com/a741424975game/django-admin-history-detail',
    license='MIT',
    author='Gzp',
    author_email='741424975@qq.com',
    keywords="django admin",
    description='Make model change history show more detail',
    zip_safe=False,
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)
