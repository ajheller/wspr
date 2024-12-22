#!/usr/bin/env python

""" Code to encode WSPR message
"""

import string
import re
import numpy as np

# pylint: disable=missing-function-docstring

# References
#  https://www.arrl.org/wspr
#  https://swharden.com/software/FSKview/wspr/
#  https://en.m.wikipedia.org/wiki/WSPR_(amateur_radio_software)
#  http://www.g4jnt.com/Coding/WSPR_Coding_Process.pdf
#
# Bit manipulation in Python
#  https://wiki.python.org/moin/BitManipulation
#
# also:
#  https://www.levinecentral.com/ham/grid_square.php
#  https://www.karhukoti.com/maidenhead-grid-square-locator
#  https://users.cecs.anu.edu.au/~Gerard.Borg/anu/projects/amateur/wsprnet/wsprnet.html
#
# other Python versions:
#  https://github.com/PH0TRA/wspr
#  http://blog.marxy.org/2024/09/python-code-to-generate-wspr-audio-tones.html
#  https://gist.github.com/peterbmarks/339e5ae83b5351151137679b8f527466
#

# Call sign encoding
# The third character MUST be a number. To cope with callsigns that start letter
# followed by a number, a space is appended to the front if necessary. So, for
# example, G4JNT will become [sp]G4JNT whereas GD4JNT stays as-is.
#
# Short callsigns are then further padded out to six characters by appending spaces
# to the end.
#
# The 37 allowed characters are allocated values from 0 to 36 such that ‘0’ – ‘9’
# give 0 – 9, ‘A’ to ‘Z’ give 10 to 35 and [space] is given the value 36.
#
# Further coding rules on callsigns mean that the final three characters (of the
# now padded out callsign) can only be letters or [sp] so will only take the values
# 10 – 36.
#
# With the characters, designated [Ch X], taking on values from 0 to 36 as defined,
# the callsign is now compressed into a single integer N by successively building up.


def normalize_callsign(callsign):
    idx = None
    for idx, ch in enumerate(callsign):
        if ch in string.digits:
            break
    newcallsign = 6 * [" "]
    newcallsign[2 - idx : 2 - idx + len(callsign)] = callsign
    return "".join(newcallsign)


def to_bin(v, w):
    return np.binary_repr(v, w)


def encode_callsign(callsign):
    callsign = callsign.upper()
    callsign = normalize_callsign(callsign)
    lds = string.digits + string.ascii_uppercase + " "
    ld = string.digits + string.ascii_uppercase
    d = string.digits
    ls = string.ascii_uppercase + " "
    acc = lds.find(callsign[0])
    acc *= len(ld)
    acc += ld.find(callsign[1])
    acc *= len(d)
    acc += d.find(callsign[2])
    acc *= len(ls)
    acc += ls.find(callsign[3])
    acc *= len(ls)
    acc += ls.find(callsign[4])
    acc *= len(ls)
    acc += ls.find(callsign[5])
    return to_bin(acc, 28)  # binary string 28-bits wide


GRID_SQUARE_RE = re.compile("[A-R][A-R][0-9][0-9]([a-x][a-x])?$")


def grid2ll(grid):
    if not GRID_SQUARE_RE.match(grid):
        raise RuntimeError("Malformed grid referense ", grid)

    p = ord(grid[0]) - ord("A")
    p *= 10
    p += ord(grid[2]) - ord("0")
    p *= 24
    if len(grid) == 4:
        p += 12
    else:
        p += (ord(grid[4]) - ord("a")) + 0.5
    lng = (p / 12) - 180.0
    p = ord(grid[1]) - ord("A")
    p *= 10
    p += ord(grid[3]) - ord("0")
    p *= 24
    if len(grid) == 4:
        p += 12
    else:
        p += (ord(grid[5]) - ord("a")) + 0.5
    lat = (p / 24) - 90.0

    return (lat, lng)


def encode_grid(grid):
    grid = grid.upper()
    lat, long = grid2ll(grid)
    long = int((180 - long) / 2.0)
    lat = int(lat + 90.0)
    return to_bin(long * 180 + lat, 15)


def encode_power(power):
    if power.isdigit() and len(power) == 2:
        power = int(power)
        power = power + 64

    else:
        raise RuntimeError("Malformed power value ", power)

    return to_bin(power, 7)


def bit_count(int_type):
    count = 0
    while int_type:
        int_type &= int_type - 1
        count += 1
    return count

def parity_of(int_type):
    return bit_count(int_type) & 1


def parity(x):
    even = 0
    while x:
        even = 1 - even
        x = x & (x - 1)
    return even


def bitstring(x):
    return "".join([str((x >> i) & 1) for i in range(8)[::-1]])


def bitreverse(x):
    bs = bitstring(x)
    return int(bs[::-1], 2)


def convolver(bit, acc):
    acc = ((acc << 1) & 0xFFFFFFFF) | bit
    return parity(acc & 0xF2D05351), parity(acc & 0xE4613C47), acc


def encode(l):
    f = []
    acc = 0
    l = list(map(int, list(l)))
    for x in l:
        b0, b1, acc = convolver(x, acc)
        f.append(b0)
        f.append(b1)
    return f
