#!/usr/bin/env python3

"""
Code to generate WSPR signal file
"""

import numpy as np
import scipy.signal as sig
from scipy.io import wavfile as wav
from matplotlib import pyplot as plt

import genwsprcode as gw

# pylint: disable=missing-module-docstring

# References
#  https://swharden.com/software/FSKview/wspr/
#  https://en.m.wikipedia.org/wiki/WSPR_(amateur_radio_software)
#  http://www.g4jnt.com/Coding/WSPR_Coding_Process.pdf

""" testing
python wspr_signal.py
sox wspr.wav -n stats spectrogram
open spectrogram.png
open wspr.wav
play wspr.wav   # play is part of sox

"""

CALLSIGN = "AK6IM"
GRID = "CM87"  # San Mateo County
POWER = "10"  # dBm


WSPR_SAMPLE_RATE = 8000  # Sa/sec
WSPR_BASE_FREQUENCY = 1500  # hz
WSPR_KEYING_RATE = 12000 / 8192  # symbols/sec
WSPR_TONE_SEPARATION = WSPR_KEYING_RATE  # Minimum-shift keying
WSPR_SYMBOL_DURATION = 1 / WSPR_KEYING_RATE  # seconds

print(
    f"{WSPR_SAMPLE_RATE=}"
    f"\n{WSPR_BASE_FREQUENCY=}"
    f"\n{WSPR_KEYING_RATE=}"
    f"\n{WSPR_TONE_SEPARATION=}"
    f"\n{WSPR_SYMBOL_DURATION=}"
)


def moyel(x, w=8, dim=0, in_place=False):
    """tapers the tips"""
    if not in_place:
        x = x.copy()
    win = sig.windows.hann(2 * w, sym=True)
    x[:w] *= win[:w]
    x[-w:] *= win[-w:]
    return x


symbols = np.array(gw.Genwsprcode(CALLSIGN, GRID, POWER))

samples_per_symbol = int(
    WSPR_SYMBOL_DURATION * WSPR_SAMPLE_RATE
)  # this should be an integer

symbol_frequencies = symbols * WSPR_TONE_SEPARATION + WSPR_BASE_FREQUENCY


if True:
    # wspr is continus phase fsk
    radians_per_sample = (2 * np.pi * symbol_frequencies / WSPR_SAMPLE_RATE).astype(
        np.float64
    )
    dphi = np.tile(radians_per_sample, (samples_per_symbol, 1)).T.ravel()
    phi = np.cumsum(dphi)
    x = 0.5 * np.exp(1j * phi)
else:
    # simple way for debugging
    #   don't use, phase discontinuities create a subharmonc
    f = np.tile(symbol_frequencies, (samples_per_symbol, 1)).T.ravel()
    t = np.arange(len(f)) / WSPR_SAMPLE_RATE
    x = 0.5 * np.exp(2j * np.pi * f * t)

if True:
    # pad to 120 sec, so we can loop it
    x = moyel(x, w=int(WSPR_SAMPLE_RATE / 10), in_place=True)
    x = np.pad(
        x,
        (WSPR_SAMPLE_RATE, 119 * WSPR_SAMPLE_RATE - len(x)),
        mode="constant",
        constant_values=0j,
    )

if False:
    plt.plot(symbols)
    plt.show()
    plt.plot(symbol_frequencies)
    plt.show()
    plt.plot(radians_per_sample)
    plt.show()
    plt.plot(dphi)
    plt.show()
    plt.plot(phi)
    plt.show()


xx = x.view(np.float64).reshape(-1, 2)
wav.write("wspr.wav", WSPR_SAMPLE_RATE, xx.astype(np.float32))


print(WSPR_SYMBOL_DURATION * WSPR_SAMPLE_RATE)
