import os

from setuptools import setup

setup(
	name='ipmongo',
	version='0.1.2',
	description='Provide conversion of ipaddr object for MongoDB',
	long_description='Convert ipaddr object before inserting it into MongoDB; convert the data selected from MongoDB back to ipaddr object',
	url='https://github.com/wal1ybot/ipmongo',
	license='MIT',
	author='wal1ybot',
	py_modules=['ipmongo'],
	install_requires=['pymongo', 'ipaddr'],
	include_package_data=True,
	classifiers=[
		'Intended Audience :: Developers',
		'Natural Language :: English',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Programming Language :: Python :: 2.7',
		'Topic :: Software Development :: Libraries :: Python Modules',
		'Topic :: Database',
		'Topic :: System :: Networking',
	],
)
