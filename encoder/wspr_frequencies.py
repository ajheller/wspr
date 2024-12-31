#!/usr/bin/env python3

"""WSPR frequencies
"""
# pylint: disable=pointless-string-statement

# from http://www.wsprnet.org/drupal/sites/wsprnet.org/files/wspr-qrg.pdf
""" 
Band Dial Band Start Band End
160m 1 836,6 kHz 1 838,0 kHz 1 838,2 kHz
80m 3 568,6 kHz 3 570,0 kHz 3 570,2 kHz
60m 5 287,2 kHz 5 288,6 kHz 5 288,8 kHz
40m 7 038,6 kHz 7 040,0 kHz 7 040,2 kHz
30m 10 138,7 kHz 10 140,1 kHz 10 140,3 kHz
20m 14 095,6 kHz 14 097,0 kHz 14 097,2 kHz
17m 18 104,6 kHz 18 106,0 kHz 18 106,2 kHz
15m 21 094,6 kHz 21 096,0 kHz 21 096,2 kHz
12m 24 924,6 kHz 24 926,0 kHz 24 926,2 kHz
10m 28 124,6 kHz 28 126,0 kHz 28 126,2 kHz
6m 50 293,0 kHz 50 294,4 kHz 50 294,6 kHz
2m 144 488,5 kHz 144 489,9 kHz 144 490,1 kHz
"""


# from https://www.sigidwiki.com/wiki/WSPR
#  Note these are 'dial frequencies' the WSPR band is 1400-1600 Hz above these.
"""
136 kHz
474.2 kHz
1.8366 MHz
3.5686 MHz
7.0386 MHz
10.1387 MHz
14.0956 MHz
18.1046 MHz
21.0946 MHz
24.9246 MHz
28.1246 MHz
50.2930 MHz (Region 2, 3)
70.0910 MHz (Region 1)
70.1510 MHz
144.4890 MHz
432.3000 MHz
1.2965 GHz
"""
wspr_frequencies = (
    136e3,
    474.2e3,
    1.8366e6,
    3.5686e6,
    7.0386e6,
    10.1387e6,
    14.0956e6,
    18.1046e6,
    21.0946e6,
    24.9246e6,
    28.1246e6,
    50.2930e6,  # Region 2, 3
    70.0910e6,  # Region 1
    70.1510e6,
    144.4890e6,
    432.3000e6,
    1.2965e9,
)

wspr_bands = (2200, 630, 160, 80, 40, 40, 20, 17, 15, 12, 10, 6, 4, 2, 0.7, 0.25)
