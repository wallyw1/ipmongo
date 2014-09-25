#!/usr/bin/env python

"""
The MIT License (MIT)

Copyright (c) 2004 wal1ybot

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from pymongo.son_manipulator import SONManipulator
from ipaddr import IPAddress, IPNetwork
from ipaddr import IPv4Address, IPv4Network
from ipaddr import IPv6Address, IPv6Network

def encode_ipaddress(ip):

	# Determine _type (IPAddress or IPNetwork) for describing the data in MongoDB.
	# The object is actually stored in str in MongoDB.
	if isinstance(ip, (IPv4Address, IPv6Address)):
		_type = 'IPAddress'
		ip_repr = str(ip)
	elif isinstance(ip, (IPv4Network, IPv6Network)):
		_type = 'IPNetwork'
		ip_repr = str(ip)

	return {'_type': _type, 'ip': ip_repr}

def decode_ipaddress(doc):

	# Check whether IPAddress or IPNetwork in _type returned from MongoDB.
	assert doc['_type'] == 'IPAddress' or doc['_type'] == 'IPNetwork'

	# Convert to ipaddr object according to _type
	if doc['_type'] == 'IPAddress':
		return IPAddress(doc['ip'])
	elif doc['_type'] == 'IPNetwork':
		return IPNetwork(doc['ip'])

class TransformIP(SONManipulator):
	def transform_incoming(self, son, coll):

		# Determine type of son to get (key, val) iter_items.
		if isinstance(son, (list, set)):
			iter_items = enumerate(son)
		elif isinstance(son, dict):
			iter_items = son.items()

		# Break into (key, val) so that examine each val.
		# If val is a type in ipaddr, encode it into int (IPv4) or str (IPv6).
		for (key, val) in iter_items:
			if isinstance(val, (IPv4Address, IPv4Network, IPv6Address, IPv6Network)):
				son[key] = encode_ipaddress(val)
			elif isinstance(val, (list, set, dict)):
				son[key] = self.transform_incoming(val, coll)

		return son

	def transform_outgoing(self, son, coll):

		# Watch any _type in record returned from MongoDB.
		# If _type is IPAddress or IPNetwork, decode it.
		# If no _type found in the record, watch its val recursively.
		for (key, val) in son.items():
			if isinstance(val, dict):
				if '_type' in val and val['_type'] in ('IPAddress', 'IPNetwork'):
					son[key] = decode_ipaddress(val)
				else:
					son[key] = self.transform_outgoing(val, coll)

		return son
