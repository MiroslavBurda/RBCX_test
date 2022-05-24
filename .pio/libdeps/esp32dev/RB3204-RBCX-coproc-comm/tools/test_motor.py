#!/usr/bin/env python3

import random
import serial
import sys
import time
import threading
from google.protobuf import text_format

from lib import frame_send, frame_receive
import rbcx_pb2 as pb

def read_serial(port):
    while True:
        msg = frame_receive(port, pb.CoprocStat);
        if msg.powerAdcStat is None:
            print(text_format.MessageToString(msg, as_one_line=True))


if __name__ == "__main__":
    with serial.Serial(sys.argv[1], baudrate=921600) as port:
        threading.Thread(target=read_serial, args=(port, ), daemon=True).start()
        motorIndex = int(sys.argv[2]) if len(sys.argv) > 2 else 1
        p = int(input("P:"))
        i = int(input("I:"))
        d = int(input("D:"))
        a = int(input("AccMax:"))
        msg = pb.CoprocReq(motorReq=pb.CoprocReq.MotorReq(motorIndex=motorIndex, setPositionRegCoefs=pb.RegCoefs(p=p, i=i, d=d)))
        frame_send(port, msg)
        msg = pb.CoprocReq(motorReq=pb.CoprocReq.MotorReq(motorIndex=motorIndex, setConfig=pb.MotorConfig(maxAccel=1000)))
        frame_send(port, msg)
        while True:
            position = int(input())
            msg = pb.CoprocReq(motorReq=pb.CoprocReq.MotorReq(motorIndex=motorIndex, addPosition=position))
            frame_send(port, msg)
