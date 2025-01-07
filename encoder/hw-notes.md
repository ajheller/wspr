# QPR transmitter notes

## Cheap RF amps from Amazon

1. <https://www.amazon.com/dp/B0CFLB7QLF>  -- "9-12V Radio Frequency Wideband Amplifier Low Noise Amplifier LNA 0.1-2000MHz Gain 32dB"
    * 32 dB gain,
    * max out 13 dBm (20 mW)  
    * 9-12V, 27 mA
    * $8.99

2. <https://www.amazon.com/gp/product/B09HX3C43K/> -- "Amplifier Module 1-930MHz Working Frequency 2.0W Professional RF Amplifier Module with Stable Performance"  
    * input power 0 dBm,
    * output power 33 dBm (2 W),
    * 12V 3-400 mA, (regulator is a 7905, should run off 6.1V - 1.1 V dropout)
    * $11.29

3. <https://www.amazon.com/gp/product/B08DNYQQHL/> -- "RF Power Amplifier 1MHz-700MHZ 3.2W HF VHF UHF Transmitter Power Amplifier Module for Ham Radio"
    * input power 0 dBm,
    * output power 35 dBm (3.2 W),
    * 15V 350 mA, (regulator is a 7909, should run off 10.1 V)
    * $36.69

4. <https://www.ebay.com/itm/30W-Shortwave-Power-Amplifier-Board-CW-SSB-Linear-High-Frequency-Power-Amplifier-/326100331135> -- 30W Shortwave Power Amplifier Board CW SSB Linear High Frequency Power Amplifier
    * input power 0.1 - 3W
    * frequency range 3-28 MHz
    * \$23 + \$3.50 shipping

Connecting the TinySA directly to the HackRF, I see about -1 dBm output with the TX gain set to +47 dB.  The 14 dB amp has no effect.  

Connecting amp #2 directly to the HackRF, then through a 40 dB pad to the TinySA, I see about -8 dBm, which is +32 dBm (1.8W) going into the pad.

## Output filter bank

1. <https://www.ebay.com/itm/111975498088> -- "Assembled 12v 100W 3.5Mhz-30Mhz HF power amplifier low pass filter LPF"

## HackRF notes

<https://hackrf.readthedocs.io/en/latest/sampling_rate.html> says:

* _Using a sampling rate of less than 8MHz is not recommended. Partly, this is because the MAX5864 (ADC/DAC chip) isn’t specified to operate at less than 8MHz, and therefore, no promises are made by Maxim about how it performs. But more importantly, the baseband filter in the MAX2837 has a minimum bandwidth of 1.75MHz. It can’t provide enough filtering at 2MHz sampling rate to remove substantial signal energy in adjacent spectrum (more than +/-1MHz from the tuned frequency). The MAX2837 datasheet suggests that at +/-1MHz, the filter provides only 4dB attenuation, and at +/-2MHz (where a signal would alias right into the center of your 2MHz spectrum), it attenuates about 33dB. That’s significant._

NOTE: This might apply to RX only.

### command line

```text
(radio) heller@AIC-CAS0010705-Crean wspr % hackrf_transfer           
specify one of: -t, -c, -r, -w
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
````
