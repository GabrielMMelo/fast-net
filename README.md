# fast-net-tools

## Usage
```
usage: fastnettools.py [-h] [-t] [-d] [-T MAX_TTL] [-c COUNTS] address

positional arguments:
  address               Destination address with ICMP server if using
                        traceroute (-t) parameter, or TCP server address if
                        using downloadrate (-d) parameter

optional arguments:
  -h, --help            show this help message and exit
  -t, --traceroute      Execute traceroute tool for `address`
  -d, --downloadrate    Test download rate transfer
  -T MAX_TTL, --max_ttl MAX_TTL
                        Max TTL counter
  -c COUNTS, --count COUNTS
                        Number of pings for each router
```
