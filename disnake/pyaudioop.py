# SPDX-License-Header: MIT
# Copyright (c) 2011 James Robert, http://jiaaro.com

import struct
from ctypes import create_string_buffer

__all__ = ("mul",)


class error(Exception):
    pass


def _check_size(size):
    if size != 1 and size != 2 and size != 4:
        raise error("Size should be 1, 2 or 4")


def _check_params(length, size):
    _check_size(size)
    if length % size != 0:
        raise error("not a whole number of frames")


def _sample_count(cp, size):
    return len(cp) / size


def _get_samples(cp, size, signed=True):
    for i in range(_sample_count(cp, size)):
        yield _get_sample(cp, size, i, signed)


def _struct_format(size, signed):
    if size == 1:
        return "b" if signed else "B"
    elif size == 2:
        return "h" if signed else "H"
    elif size == 4:
        return "i" if signed else "I"


def _get_sample(cp, size, i, signed=True):
    fmt = _struct_format(size, signed)
    start = i * size
    end = start + size
    return struct.unpack_from(fmt, bytes(cp)[start:end])[0]


def _put_sample(cp, size, i, val, signed=True):
    fmt = _struct_format(size, signed)
    struct.pack_into(fmt, cp, i * size, val)


def _get_maxval(size, signed=True):
    if signed and size == 1:
        return 0x7F
    elif size == 1:
        return 0xFF
    elif signed and size == 2:
        return 0x7FFF
    elif size == 2:
        return 0xFFFF
    elif signed and size == 4:
        return 0x7FFFFFFF
    elif size == 4:
        return 0xFFFFFFFF


def _get_minval(size, signed=True):
    if not signed:
        return 0
    elif size == 1:
        return -0x80
    elif size == 2:
        return -0x8000
    elif size == 4:
        return -0x80000000


def _get_clipfn(size, signed=True):
    maxval = _get_maxval(size, signed)
    minval = _get_minval(size, signed)
    return lambda val: max(min(val, maxval), minval)


def mul(cp, size, factor):
    _check_params(len(cp), size)
    clip = _get_clipfn(size)

    result = create_string_buffer(len(cp))

    for i, sample in enumerate(_get_samples(cp, size)):
        sample = clip(int(sample * factor))
        _put_sample(result, size, i, sample)

    return result.raw
