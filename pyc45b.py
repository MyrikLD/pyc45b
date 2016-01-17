# -*- coding: utf-8 -*-
from __future__ import print_function
from sys import exit, argv
from time import sleep
from platform import system

__AUTHOR__ = "Myrik"
__CONTACT__ = "Myrik260138@tut.by"

import serial


def symb(r):
    if r == '*':
        print(r)
        return 0
    elif r == '.':
        print(r, end='')
        return 0
    elif r == '+':
        print ("End")
        return 1
    elif r == '-':
        print("Chechsum error")
        return 2
    else:
        print("Unknown resp:" + r)
        return 2


def main():
    args = argv
    args.pop(0)
    # args.append("-p COM9")
    # args.append("-f C:\\Hex.hex")

    baud = 115200
    faddr = ''
    ser = ''
    proto = '232'

    for a in args:
        if a[0] == '-':
            cmd = a[1]
            a = a[2:]
        else:
            continue

        if cmd == 'p':
            ser = a
            if system() == "Windows":
                ser = int(a[3:]) - 1
        elif cmd == 'f':
            faddr = a
        elif cmd == 'b':
            baud = int(a)
        elif cmd == 's':
            proto = a

    if len(args) < 2 or faddr == '' or ser == '':
        print("Using:")
        print("Windows: pyc45b.py -pCOM1 -b115200 -s232 -fhexfile.hex")
        print("Linux: pyc45b.py -p/dev/ttyUSB0 -b115200 -s232 -fhexfile.hex")
        exit(-1)

    try:
        ser = serial.Serial(ser, baud, xonxoff=True, timeout=0)
    except serial.SerialException, e:
        print("Serial error: " + e.message)
        exit(-1)

    if proto == '485':
        print("RS485:"+str(baud))
    elif proto == '232':
        print("RS232:"+str(baud))
    else:
        print("Unknown protocol: "+proto)
        exit(0)

    print("Waiting for reset MCU")

    resp = ''
    # while resp == '' or resp == '\x00':
    tic = 0
    while resp != 'c':
        if proto == '485':
            ser.write('UUUUUUUUUU ')
        else:
            ser.write('U')
        sleep(0.1)
        resp = ser.read(1)

    sleep(0.1)
    resp += ser.readall()
    if resp[:5] == "c45b2":
        print("Bootloader version: " + resp[:-3])
    else:
        print("Sync error")
        exit(-1)

    sleep(0.1)
    ser.write('pf\r\n')

    tick = 0
    while resp != 'p':
        resp = ser.read(1)
        tick += 1
        sleep(0.1)
        if tick > 100:
            print("progMode timeout")
            exit(-1)
    resp += ser.read(2)

    if resp[2] == '+':
        ser.flushInput()
        print("Start uploading")
    else:
        print("progMode error: " + resp)
        exit(-1)

    resp = ()
    try:
        with open(faddr) as f:
            for line in f:
                ser.write(line)
                while len(resp) == 0:
                    resp = list(ser.readall())
                while len(resp) != 0:
                    r = symb(resp.pop(0))
                    if r == 1:
                        break
                    elif r == 2:
                        exit(-1)
    except Exception as e:
        print("Error: "+e.args[1])
        exit(0)

    sleep(0.1)

    while len(resp) == 0:
        resp = list(ser.readall())
        
    while len(resp) != 0:
        r = symb(resp.pop(0))
        if r == 1:
            break
        elif r == 2:
            exit(-1)

    print("Run programm...", end='')
    ser.write('g\n')
    sleep(1)
    resp = ser.readall()
    if resp[:2] == "g+":
        print("Successful!")
    else:
        print("Fail!")
        exit(-1)
    ser.close()
    exit(0)


if __name__ == '__main__':
    main()
