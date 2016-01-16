# pyc45b
<p>pyc45b is a frontend to the AVR bootloader from Chip45 writing on python</p>
(see <a href='http://www.chip45.com/info/chip45boot2.html'>http://www.chip45.com/info/chip45boot2.html</a> for details).

<p>Typical use:</p>
    pyc45b.py -p[SERIAL] -b[BAUD] -s[STANDARD] -f[FILE.hex]
    Windows: pyc45b.py -pCOM1 -b115200 -s232 -fhexfile.hex
    Linux: pyc45b.py -p/dev/ttyUSB0 -b9600 -s232 -ffile.hex

MyrikLD[BY] Aug2015
