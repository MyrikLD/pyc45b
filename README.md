# pyc45b
<p>pyc45b is a frontend to the AVR bootloader from Chip45 writing on python</p>
(see <a href='http://www.chip45.com/info/chip45boot2.html'>http://www.chip45.com/info/chip45boot2.html</a> for details).

<p>Typical use:</p>
    Windows: pyc45b.py -p COM1 -b 115200 -f hexfile.hex
    Linux: pyc45b.py -p /dev/ttyUSB0 -b 115200 -f hexfile.hex