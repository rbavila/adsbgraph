#!/usr/bin/env python3
import argparse
import sys
import signal
from TCPWorker import TCPWorker
from BEASTWorker import BEASTWorker
from ModeSMessage import ModeSMessage
from DataWorker import DataWorker
from RRDWorker import RRDWorker


def sig_handler(sig, frame):
    print("Terminating... ", end="", file=sys.stderr)
    rw.update_lock.acquire()
    print("done.", file=sys.stderr)
    sys.exit(0)


#
# main
#
parser = argparse.ArgumentParser(description="Monitora o ADS-B.")
parser.add_argument("host")
parser.add_argument("port")
parser.add_argument("m_rrdfile")
parser.add_argument("r_rrdfile")
parser.add_argument("--grdir", default=".")
args = parser.parse_args()

signal.signal(signal.SIGINT, sig_handler)
signal.signal(signal.SIGTERM, sig_handler)
tw = TCPWorker(args.host, args.port)
bw = BEASTWorker(tw.buffer)
dw = DataWorker(bw.msgqueue)
rw = RRDWorker(dw.stats, dw.rr, args.m_rrdfile, args.r_rrdfile, args.grdir)
tw.start()
bw.start()
dw.start()
rw.start()
tw.join()
bw.join()
dw.join()
rw.join()
