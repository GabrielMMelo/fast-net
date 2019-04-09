#!/usr/bin/env python

import argparse

import traceroute
import downloadrate

parser = argparse.ArgumentParser()
parser.add_argument("address", help="Destination address with ICMP server if using traceroute (-t) parameter, or TCP server address if using downloadrate (-d) parameter")
parser.add_argument("-t", "--traceroute", action="store_true", dest="traceroute", default=False, help="Execute traceroute tool for `address`")
parser.add_argument("-d", "--downloadrate", action="store_true", dest="downloadrate", default=False, help="Test download rate transfer")
parser.add_argument("-T", "--max_ttl", dest="max_ttl", type=int, default=30, help="Max TTL counter")
parser.add_argument("-c", "--count", dest="counts", type=int, default=3, help="Number of pings for each router")
args = parser.parse_args()

if __name__ == '__main__':
    if args.traceroute:
        traceroute.Traceroute(args.address, max_ttl=args.max_ttl+1, counts=args.counts+1)
    elif args.downloadrate:
        downloadrate.DownloadRate(args.address)
