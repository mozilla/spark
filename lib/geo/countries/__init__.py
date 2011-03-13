"""
This list of localized country names is borrowed from:
http://svn.mozilla.org/libs/product-details/json/regions/
"""
import json
import os

countries = {}
root = os.path.dirname(os.path.realpath(__file__))

for filename in os.listdir(root):
    if filename.endswith('.json'):
        name = os.path.splitext(filename)[0]
        path = os.path.join(root, filename)
        countries[name] = json.load(open(path))