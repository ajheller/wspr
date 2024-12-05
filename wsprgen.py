#!/usr/bin/env python3
# Pure python code to generate WSPR audio tones
#
# Heavily based on https://github.com/PH0TRA/wspr which drove an AD9851
# I removed that code and replaced it with audio generation using pyaudio
# wsprgen.py CALLSIGN GRID dBPower BASE_AUDIO_FREQUENCY

# genwsprcode from https://github.com/PH0TRA/wspr/blob/master/genwsprcode.py
import genwsprcode as g
import pyaudio
import numpy as np
import time
import sys
from optparse import OptionParser
from random import randrange


def main():
    # set variables
    freq_shift = 12000 / 8192
    offset = 0

    usage = "wspr.py [options] callsign grid power[dBm] frequency1[Hz] <frequency2>..."
    usage_freq = 'frequency in Hz or standard WSPR frequency e.g. "14097100" or "10m"'

    p = OptionParser(usage=usage)
    p.add_option(
        "-n",
        "--no-delay",
        action="store_true",
        dest="nowait",
        help="Transmit immediately, do not wait for a WSPR TX window. "
        + " Used for testing only",
    )
    p.add_option(
        "-r",
        "--repeat",
        action="store_true",
        dest="repeat",
        help="Repeat endless untill ctrl-c is pressed",
    )
    p.add_option(
        "-o",
        "--offset",
        action="store_true",
        dest="offset",
        help="Add a random offset between -80 and 80 Hz from center frequency",
    )
    p.add_option(
        "-t",
        "--testtone",
        action="store_true",
        dest="tone",
        help="Simply output a test tone at the specified frequency. "
        + "For debugging and to verify calibration",
    )

    (opts, args) = p.parse_args()

    if opts.tone:
        frequencies = args[0 : len(args)]
    else:
        try:
            callsign = args[0]
            grid = args[1]
            power = args[2]
            frequencies = args[3 : len(args)]
        except:
            print("Malformed arguments.", file=sys.stderr)
            print(usage, file=sys.stderr)
            sys.exit(-1)

        # frequency=int(frequency)
        symbols = g.Genwsprcode(callsign, grid, power)
        symbols = symbols.rstrip(",")
        print("symbols\n", symbols)
        symbols = symbols.split(",")

    # PyAudio configuration
    sample_rate = 44100  # CD quality sample rate

    # Function to generate a sine wave for a note
    def generate_tone(frequency, duration, sample_rate=44100):
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        tone = 0.5 * np.sin(2 * np.pi * frequency * t)
        return (tone * np.iinfo(np.int16).max).astype(np.int16)

    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Open an audio stream
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=sample_rate, output=True)

    if not opts.nowait or not opts.tone:
        print("Waiting for next WSPR TX window...")

    while True:
        for frequency in frequencies:  # get the frequencies from the list
            try:
                frequency = int(frequency)  # else it must be an integer value
            except:
                print("Malformed frequency.", file=sys.stderr)
                print(usage_freq, file=sys.stderr)
                sys.exit(-1)

            if not opts.nowait:  # check wether nowait
                past_time_window = time.time() % 120
                time.sleep(120 - past_time_window)

            if frequency == 0:
                print(
                    "Skipping transmission on:",
                    time.strftime("%H:%M:%S", time.gmtime(time.time())),
                )
                time.sleep(110)
            elif opts.tone:
                print(
                    "Start of test tone on:",
                    time.strftime("%H:%M:%S", time.gmtime(time.time())),
                )
                print("Frequency: {0:,.0f} Hz".format(frequency))
                samples = generate_tone(frequency, duration)
                stream.write(samples.tobytes())
                time.sleep(120)
                reset()
                print(
                    "End of test tone on:",
                    time.strftime("%H:%M:%S", time.gmtime(time.time())),
                )
            else:
                if opts.offset:
                    frequency = frequency + randrange(-80, 81)

                print(
                    "Start of transmission on:",
                    time.strftime("%H:%M:%S", time.gmtime(time.time())),
                )
                print("Frequency: {0:,.0f} Hz".format(frequency))

                for symbol in symbols:  # modulate the symbols
                    freq_shift = 12000 / 8192
                    fsk = float(symbol) * freq_shift
                    duration = 0.683
                    out_frequency = frequency + fsk
                    print(f"symbol = {symbol}, out_frequency = {out_frequency}")
                    samples = generate_tone(out_frequency, duration)
                    stream.write(samples.tobytes())

                print(
                    "End of transmission on:",
                    time.strftime("%H:%M:%S", time.gmtime(time.time())),
                )
        if not opts.repeat:
            break


def reset():
    print("reset()")


if __name__ == "__main__":
    main()
