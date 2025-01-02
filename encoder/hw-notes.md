# QPR transmitter notes

Amps from Amazon
 * https://www.amazon.com/dp/B0CFLB7QLF  -- 32 dB gain, max out 13 dBm (20 mW)  $8.99
 * https://www.amazon.com/gp/product/B09HX3C43K/ -- input power 0 dBm, output power 33 dBm (2 W), 12V 3-400 mA, $11.29
 * https://www.amazon.com/gp/product/B08DNYQQHL/ -- input power 0 dBm, output power 35 dBm (3.2 W), 15V 350 mA, $36.69

Connecting the TinySA directly to the HackRF, I see about -1 dBm output with the TX gain set to +47 dB.  The 14 dB amp has no effect.  

Connecting the amps directly to the HackRF, then through a 40 dB pad to the TinySA, I see about -8 dBm, which is +32 dBm going into the pad.
