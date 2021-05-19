__version__ = '1.0.0'
__all__ = [
    'Json'
]

__author__ = 'CACode <cacode@163.com>'

from . import _default_encoder, JSONEncoder, _default_decoder, JSONDecoder
from decimal import Decimal


class Json:

    @staticmethod
    def dumps(obj, skipkeys=False, ensure_ascii=True, check_circular=True,
              allow_nan=True, cls=None, indent=None, separators=None,
              encoding='utf-8', default=None, use_decimal=True,
              namedtuple_as_object=True, tuple_as_array=True,
              bigint_as_string=False, sort_keys=False, item_sort_key=None,
              for_json=False, ignore_nan=False, int_as_string_bitcount=None,
              iterable_as_array=False, **kw):
        """
            转json字符串
        """
        if (not skipkeys and ensure_ascii and
                check_circular and allow_nan and
                cls is None and indent is None and separators is None and
                encoding == 'utf-8' and default is None and use_decimal
                and namedtuple_as_object and tuple_as_array and not iterable_as_array
                and not bigint_as_string and not sort_keys
                and not item_sort_key and not for_json
                and not ignore_nan and int_as_string_bitcount is None
                and not kw
        ):
            return _default_encoder.encode(obj)
        if cls is None:
            cls = JSONEncoder
        return cls(
            skipkeys=skipkeys, ensure_ascii=ensure_ascii,
            check_circular=check_circular, allow_nan=allow_nan, indent=indent,
            separators=separators, encoding=encoding, default=default,
            use_decimal=use_decimal,
            namedtuple_as_object=namedtuple_as_object,
            tuple_as_array=tuple_as_array,
            iterable_as_array=iterable_as_array,
            bigint_as_string=bigint_as_string,
            sort_keys=sort_keys,
            item_sort_key=item_sort_key,
            for_json=for_json,
            ignore_nan=ignore_nan,
            int_as_string_bitcount=int_as_string_bitcount,
            **kw).encode(obj)

    @staticmethod
    def loads(s, encoding=None, cls=None, object_hook=None, parse_float=None,
              parse_int=None, parse_constant=None, object_pairs_hook=None,
              use_decimal=False, **kw):
        """
        json转字典
        """
        if (cls is None and encoding is None and object_hook is None and
                parse_int is None and parse_float is None and
                parse_constant is None and object_pairs_hook is None
                and not use_decimal and not kw):
            return _default_decoder.decode(s)
        if cls is None:
            cls = JSONDecoder
        if object_hook is not None:
            kw['object_hook'] = object_hook
        if object_pairs_hook is not None:
            kw['object_pairs_hook'] = object_pairs_hook
        if parse_float is not None:
            kw['parse_float'] = parse_float
        if parse_int is not None:
            kw['parse_int'] = parse_int
        if parse_constant is not None:
            kw['parse_constant'] = parse_constant
        if use_decimal:
            if parse_float is not None:
                raise TypeError("use_decimal=True implies parse_float=Decimal")
            kw['parse_float'] = Decimal
        return cls(encoding=encoding, **kw).decode(s)
