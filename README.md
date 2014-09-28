# ipmongo

## Why need ipmongo

When using pymongo to handle ipaddr (Google's IP address manipulation library, <https://pypi.python.org/pypi/ipaddr>) object, since MongoDB does not support such object type natively, pymongo returns error.

If you want to use ipaddr object without manual conversion of the object when inserting into or selecting from MongoDB, you can use ipmongo to handle it for you automatically.

## How to install ipmongo

*   ipmongo requires pymongo (<https://pypi.python.org/pypi/pymongo/>) and ipaddr (<https://pypi.python.org/pypi/ipaddr>).
*   To install ipmongo, run `pip install ipmongo`.

## How to use ipmongo

*   In pymongo, it supports adding 'custom type': <http://api.mongodb.org/python/current/examples/custom_type.html>
*   ipmongo handles the logic of 'encoding' and 'decoding' for you. All you need to do is to add the `TransformIP()` class in ipmongo to db instance created from pymongo.
*   **IMPORTANT**:
    *   Since mutable variables are passed as reference (pointer) to any method, transformation operations in ipmongo will modify ORIGINAL content of any variable to be inserted/updated into MongoDB.
    *   To avoid any variable being modified by ipmongo, pass a copy of the variable, e.g. by calling dict() method.
*   Please refer to test.py for details: <https://github.com/wal1ybot/ipmongo/blob/master/test.py>
*   You can also download and run test.py to play with it.

## Limitations of ipmongo

*   It only supports ipaddr, Google's IP address manipulation library.
*   It only supports IPv4Address, IPv4Network, IPv6Address, IPv6Network of ipaddr.
*   It encodes the objects into str for storing in MongoDB. That means you cannot do network math on database level.
*   It assumes that you use Python built-in list, set, dict type to store these objects.

## Licence of ipmongo

ipmongo is an MIT-licensed Python module.

## Change log

### 2014-09-28: 0.1.1

*   Fixed hashbang in test.py, single quote consistency in ipmongo.py. Contributed by [Jimmy Wong](https://github.com/wyuenho).
*   Address the issue of the content of variable processed by ipmongo will be modified. Please refer to test.py for details.

### 2014-09-25: 0.1.0

*   First release
