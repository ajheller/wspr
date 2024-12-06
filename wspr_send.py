#!/usr/bin/env python3

"""
    Code to manage the HackRF One
    
(radio) heller@AIC-CAS0010705-Crean wspr % hackrf_transfer -h
Usage:
	-h # this help
	[-d serial_number] # Serial number of desired HackRF.
	-r <filename> # Receive data into file (use '-' for stdout).
	-t <filename> # Transmit data from file (use '-' for stdin).
	-w # Receive data into file with WAV header and automatic name.
	   # This is for SDR# compatibility and may not work with other software.
	[-f freq_hz] # Frequency in Hz [1MHz to 6000MHz supported, 0MHz to 7250MHz forceable].
	[-i if_freq_hz] # Intermediate Frequency (IF) in Hz [2170MHz to 2740MHz supported, 2000MHz to 3000MHz forceable].
	[-o lo_freq_hz] # Front-end Local Oscillator (LO) frequency in Hz [84MHz to 5400MHz].
	[-m image_reject] # Image rejection filter selection, 0=bypass, 1=low pass, 2=high pass.
	[-a amp_enable] # RX/TX RF amplifier 1=Enable, 0=Disable.
	[-p antenna_enable] # Antenna port power, 1=Enable, 0=Disable.
	[-l gain_db] # RX LNA (IF) gain, 0-40dB, 8dB steps
	[-g gain_db] # RX VGA (baseband) gain, 0-62dB, 2dB steps
	[-x gain_db] # TX VGA (IF) gain, 0-47dB, 1dB steps
	[-s sample_rate_hz] # Sample rate in Hz (2-20MHz supported, default 10MHz).
	[-F force] # Force use of parameters outside supported ranges.
	[-n num_samples] # Number of samples to transfer (default is unlimited).
	[-S buf_size] # Enable receive streaming with buffer size buf_size.
	[-B] # Print buffer statistics during transfer
	[-c amplitude] # CW signal source mode, amplitude 0-127 (DC value to DAC).
	[-R] # Repeat TX mode (default is off)
	[-b baseband_filter_bw_hz] # Set baseband filter bandwidth in Hz.
	Possible values: 1.75/2.5/3.5/5/5.5/6/7/8/9/10/12/14/15/20/24/28MHz, default <= 0.75 * sample_rate_hz.
	[-C ppm] # Set Internal crystal clock error in ppm.
	[-H] # Synchronize RX/TX to external trigger input.
(radio) heller@AIC-CAS0010705-Crean wspr %
"""
