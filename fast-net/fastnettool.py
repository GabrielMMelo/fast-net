import argparse

import traceroute

parser = argparse.ArgumentParser()
parser.add_argument("address", help="Destination host address")
parser.add_argument("-t", "--traceroute", action="store_true", dest="traceroute", default=False, help="Execute traceroute tool for `address`")
parser.add_argument("-T", "--max_ttl", dest="max_ttl", type=int, default=30, help="Max TTL counter")
parser.add_argument("-c", "--count", dest="counts", type=int, default=3, help="Number of pings for each router")
args = parser.parse_args()

if __name__ == '__main__':
    if args.traceroute:
        traceroute.Traceroute(args.address, max_ttl=args.max_ttl+1, counts=args.counts+1)
