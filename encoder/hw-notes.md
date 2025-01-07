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
    * $23 + $3.50 shipping

Connecting the TinySA directly to the HackRF, I see about -1 dBm output with the TX gain set to +47 dB.  The 14 dB amp has no effect.  

Connecting the amp #2 directly to the HackRF, then through a 40 dB pad to the TinySA, I see about -8 dBm, which is +32 dBm (1.8W) going into the pad.

## HackRF notes

<https://hackrf.readthedocs.io/en/latest/sampling_rate.html> says:

* _Using a sampling rate of less than 8MHz is not recommended. Partly, this is because the MAX5864 (ADC/DAC chip) isn’t specified to operate at less than 8MHz, and therefore, no promises are made by Maxim about how it performs. But more importantly, the baseband filter in the MAX2837 has a minimum bandwidth of 1.75MHz. It can’t provide enough filtering at 2MHz sampling rate to remove substantial signal energy in adjacent spectrum (more than +/-1MHz from the tuned frequency). The MAX2837 datasheet suggests that at +/-1MHz, the filter provides only 4dB attenuation, and at +/-2MHz (where a signal would alias right into the center of your 2MHz spectrum), it attenuates about 33dB. That’s significant._

NOTE: This might apply to RX only.
