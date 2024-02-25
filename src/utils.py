import collections
import json


def sorted_dict(d):
    return collections.OrderedDict(sorted(d.items()))

def pprint(d):
    print(json.dumps(d, indent=4))
