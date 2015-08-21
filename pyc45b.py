# -*- coding: utf-8 -*-
__AUTHOR__ = "Myrik"
__CONTACT__ = "Myrik260138@tut.by"

import serial
import sys
from time import sleep


def symb(r):
    if r == '*':
        print r
        return 0
    elif r == '.':
        print '.',
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
    args = sys.argv
    args.pop(0)
    if len(args) < 2:
        print "Using: c45b.py [COMPORT_NUM] [FILE_PATH].hex"
        exit(0)
    ser = serial.Serial(int(args[0][3:]) - 1, 115200, xonxoff=True, timeout=0)
    resp = ''
    print "Waiting for reset MCU"
    while resp == '' or resp == '\x00':
        ser.write('U')
        resp = ser.read(15)
    sleep(0.1)
    resp += ser.read(15)
    if resp[:5] == "c45b2":
        print resp[:-3]
    else:
        print "Sync error"
        exit(-1)
    ser.write('pf\n')
    sleep(1)
    resp = ser.read(10)
    if resp[:-2] == "pf+":
        print "Start"
    else:
        print "progMode Error: " + resp
        exit(-1)
    with open(args[1]) as f:
        for line in f:
            ser.write(line)

            resp = []
            while len(resp) == 0:
                resp = list(ser.read(10))

            while len(resp) != 0:
                r = symb(resp.pop(0))
                if r == 1:
                    break
                elif r == 2:
                    exit(-1)

    print "\nRun programm...",
    ser.write('g\n')
    sleep(1)
    resp = ser.read(10)
    if resp[:2] == "g+":
        print "Successful!"
    else:
        print "Fail!"
        exit(-1)

    file.close()
    ser.close()
    exit(0)


if __name__ == '__main__':
    main()
