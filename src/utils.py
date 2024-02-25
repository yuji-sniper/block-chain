import collections
import hashlib


def sorted_dict(d):
    return collections.OrderedDict(sorted(d.items()))
