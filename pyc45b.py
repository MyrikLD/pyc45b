# -*- coding: utf-8 -*-
__AUTHOR__ = "Myrik"
__CONTACT__ = "Myrik260138@tut.by"

import serial
from sys import exit, argv
from time import sleep
import platform


def symb(r):
    if r == '*':
        print r
        return 0
    elif r == '.':
        print r,
        return 0
    elif r == '+':
        print "End"
        return 1
    elif r == '-':
        print "Chechsum error"
        return 2
    else:
        print "Unknown resp:" + r
        return 2


def main():
    args = argv
    args.pop(0)
    # args.append("-p COM9")
    # args.append("-f C:\\Hex.hex")

    baud = 115200
    faddr = ''
    ser = ''

    for a in args:
        if a[0] == '-':
            cmd = a[1]
            a = a[2:]
        else:
            continue

        if cmd == 'p':
            ser = a
            if platform.system() == "Windows":
                ser = int(a[3:]) - 1
        elif cmd == 'f':
            faddr = a
        elif cmd == 'b':
            baud = int(a)

    if len(args) < 2 or faddr == '' or ser == '':
        print "Using:"
        print "Windows: pyc45b.py -pCOM1 -b115200 -fhexfile.hex"
        print "Linux: pyc45b.py -p/dev/ttyUSB0 -b115200 -fhexfile.hex"
        exit(-1)

    try:
        ser = serial.Serial(ser, baud, xonxoff=True, timeout=0)
    except serial.SerialException, e:
        print "Serial error: " + e.message
        exit(-1)

    print "Waiting for reset MCU"
    resp = ''
    # while resp == '' or resp == '\x00':
    while resp != 'c':
        ser.write('U')
        resp = ser.read(1)
    sleep(0.1)
    resp += ser.read(20)
    if resp[:5] == "c45b2":
        print "Bootloader version: " + resp[:-3]
    else:
        print "Sync error"
        exit(-1)
    ser.write('pf\n')
    sleep(1)
    resp = ser.read(10)
    if resp[:-2] == "pf+":
        print "Start"
    else:
        print "progMode error"
        exit(-1)

    with open(faddr) as f:
        for line in f:
            ser.write(line)

            resp = ()
            while len(resp) == 0:
                resp = list(ser.read(10))

            while len(resp) != 0:
                r = symb(resp.pop(0))
                if r == 1:
                    break
                elif r == 2:
                    exit(-1)

    print "Run programm...",
    ser.write('g\n')
    sleep(1)
    resp = ser.read(10)
    if resp[:2] == "g+":
        print "Successful!"
    else:
        print "Fail!"
        exit(-1)
    ser.close()
    exit(0)


if __name__ == '__main__':
    main()
