from __future__ import absolute_import

__version__ = '1.0.0'
__all__ = [
    'JSONDecoder', 'JSONDecodeError', 'JSONEncoder',
    'OrderedDict', 'RawJSON'
]

__author__ = 'CACode <cacode@163.com>'

from .errors import JSONDecodeError
from .raw_json import RawJSON
from .decoder import JSONDecoder
from .encoder import JSONEncoder, JSONEncoderForHTML


def _import_OrderedDict():
    import collections
    try:
        return collections.OrderedDict
    except AttributeError:
        from . import ordered_dict
        return ordered_dict.OrderedDict


OrderedDict = _import_OrderedDict()


def _import_c_make_encoder():
    try:
        from ._speedups import make_encoder
        return make_encoder
    except ImportError:
        return None


_default_encoder = JSONEncoder(
    skipkeys=False,
    ensure_ascii=True,
    check_circular=True,
    allow_nan=True,
    indent=None,
    separators=None,
    encoding='utf-8',
    default=None,
    use_decimal=True,
    namedtuple_as_object=True,
    tuple_as_array=True,
    iterable_as_array=False,
    bigint_as_string=False,
    item_sort_key=None,
    for_json=False,
    ignore_nan=False,
    int_as_string_bitcount=None,
)

_default_decoder = JSONDecoder(encoding=None, object_hook=None,
                               object_pairs_hook=None)
