#!/usr/bin/env python3
import sys
import time
from TCPWorker import TCPWorker
from BEASTWorker import BEASTWorker
from ModeSMessage import ModeSMessage
from DataWorker import DataWorker

if len(sys.argv) < 3:
    print("*** Erro: é necessário informar o servidor e a porta.",
        file=sys.stderr)
    print("Ex.: {} 192.168.0.1 30005".format(sys.argv[0]), file=sys.stderr)
    sys.exit(1)
host = sys.argv[1]
port = int(sys.argv[2])

tw = TCPWorker(host, port)
bw = BEASTWorker(tw.buffer)
dw = DataWorker(bw.msgqueue)
tw.start()
bw.start()
dw.start()

while True:
    print("---------------------------------------")
    for a in dw.aircrafts.values():
        print(a)
    time.sleep(30)
