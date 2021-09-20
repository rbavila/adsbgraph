#!/usr/bin/env python3
import sys
from TCPWorker import TCPWorker
from BEASTWorker import BEASTWorker

if len(sys.argv) < 3:
    print("*** Erro: é necessário informar o servidor e a porta.",
        file=sys.stderr)
    print("Ex.: {} 192.168.0.1 30005".format(sys.argv[0]), file=sys.stderr)
    sys.exit(1)
host = sys.argv[1]
port = int(sys.argv[2])

tw = TCPWorker(host, port)
bw = BEASTWorker(tw.buffer)
tw.start()
bw.start()

while True:
    (ts, type, mlat_ts, rssi, m) = bw.msgqueue.get()
    print(ts, type, rssi, m)
