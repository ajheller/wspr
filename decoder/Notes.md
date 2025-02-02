# notes on the wspr decoder

This code is from
  <https://github.com/WSPRpi/WSPR-Decoder>
which is a fork of
  <https://github.com/k9an/old_wsprcan>

New development is in wspr-x under:
  <https://sourceforge.net/projects/wsjt/>
  The WSPR decoder in the above repo is in FORTRAN

## Typical output

````text
  250101 0024   9  -6 -1.0 10.0015022  AK6IM CM87 10    0    1    0
````

From reading the code the fields are

* date
* UTC
* sync ?
* SNR
* time offset
* frequency [MHz]
* callsign
* grid
* tx power dBm
* drift [Hz?]
* cycles ?
* ii ?

## Format of wav file expected by wsprd

Assumes wav file is 12000 Sa/sec, 1 channel, 16-bit ints

````c
  unsigned long npoints = 114 *12000;
  short int*buf2;
  buf2 = malloc(npoints * sizeof(short int));

  nr = fread(buf2, 2, 22, fp);      // Read and ignore RIFF/WAV header
  nr = fread(buf2, 2, npoints, fp); // Read raw data

  size_t fread(void ptr[restrict .size *.nmemb],
                    size_t size, size_t nmemb,
                    FILE*restrict stream);
````

  The function fread() reads nmemb items of data, each size bytes
       long, from the stream pointed to by stream, storing them at the
       location given by ptr.

````sh
sox wspr.wav -r 12000 -c1 -b16 w.wav remix -m 1v0.1
./k9an-wsprd -H -f 28.1246 ~/dev/wspr/w.wav

(base) heller@Aarons-MacBook-Air WSPR-Decoder % ./k9an-wsprd
Usage: wsprd [options...] infile
       infile must have suffix .wav or .c2

Options:
       -e x (x is transceiver dial frequency error in Hz)
       -f x (x is transceiver dial frequency in MHz)
       -H do not use (or update) the hash table
       -n write noise estimates to file noise.dat
       -q quick mode - doesn't dig deep for weak signals
       -v verbose mode
       -w wideband mode - decode signals within +/- 150 Hz of center
(base) heller@Aarons-MacBook-Air WSPR-Decoder %
````
