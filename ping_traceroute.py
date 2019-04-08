"""
based on github open project avaliable in  https://github.com/samuel/python-ping
"""

from __future__ import print_function
import os
import sys
import socket
import struct
import select
import time
from itertools import chain
from collections import deque

if sys.platform == "win32":
    default_timer = time.clock
else:
    default_timer = time.time

# From /usr/include/linux/icmp.h; your milage may vary.
ICMP_ECHO_REQUEST = 8  # Seems to be the same on Solaris.

try:
    from reprlib import repr
except ImportError:
    pass


def checksum(source_string):
    """
    I'm not too confident that this is right but testing seems
    to suggest that it gives the same answers as in_cksum in ping.c
    """
    sum = 0
    countTo = (len(source_string)/2)*2
    count = 0
    while count < countTo:
        thisVal = ord(source_string[count + 1])*256 + ord(source_string[count])
        sum = sum + thisVal
        sum = sum & 0xffffffff  # Necessary?
        count = count + 2

    if countTo < len(source_string):
        sum = sum + ord(source_string[len(source_string) - 1])
        sum = sum & 0xffffffff  # Necessary?

    sum = (sum >> 16) + (sum & 0xffff)
    sum = sum + (sum >> 16)
    answer = ~sum
    answer = answer & 0xffff

    # Swap bytes. Bugger me if I know why.
    answer = answer >> 8 | (answer << 8 & 0xff00)

    return answer


def receive_one_ping(my_socket, ID, timeout, timeSent):
    timeLeft = timeout
    while True:
        startedSelect = default_timer()
        whatReady = select.select([my_socket], [], [], timeLeft)
        howLongInSelect = (default_timer() - startedSelect)
        if whatReady[0] == []:  # Timeout
            # print(addr)
            return "*", "*", False, False

        timeReceived = default_timer()
        recPacket, addr = my_socket.recvfrom(567)  # tamanho maximo do ICMP
        icmpHeader = recPacket[20:28]
        type, code, checksum, packetID, sequence = struct.unpack(
            "bbHHh", icmpHeader
        )

        # sucesso
        if type != 8 and packetID == ID:
            return timeReceived - timeSent, addr, True, True

        # tempo excedido ICMP
        elif type == 11:
            return timeReceived - timeSent, addr, False, True

        timeLeft = timeLeft - howLongInSelect
        if timeLeft <= 0:
            return

def send_one_ping(my_socket, dest_addr, ID):
    """
    Send one ping to the given >dest_addr<.
    """
    dest_addr = socket.gethostbyname(dest_addr)

    # Header is type (8), code (8), checksum (16), id (16), sequence (16)
    my_checksum = 0

    # Make a dummy header with a 0 checksum.
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, my_checksum, ID, 1)
    bytesInDouble = struct.calcsize("d")
    data = (192 - bytesInDouble) * "Q"
    # data = struct.pack("d", default_timer()) + data
    # print('tempo no data:', struct.unpack("d", data[:8])[0])

    # Calculate the checksum on the data and the dummy header.
    my_checksum = checksum(header + data)

    # Now that we have the right checksum, we put that in. It's just easier
    # to make up a new header than to stuff it into the dummy.
    header = struct.pack(
        "bbHHh", ICMP_ECHO_REQUEST, 0, socket.htons(my_checksum), ID, 1
    )
    # print('header size', total_size(header))
    # print('header size', total_size(header, verbose=True))
    # print('data size', total_size(data))
    packet = header + data
    # print('packet size', total_size(packet))
    # print('tempo no packet', struct.unpack('d', packet[28:28 + 8]))
    timeSent = default_timer()
    my_socket.sendto(packet, (dest_addr, 80))
    return timeSent


def do_one(dest_addr, timeout, count):
    """
    Returns either the delay (in seconds) or none on timeout.
    """
    icmp = socket.getprotobyname("icmp")
    try:
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
        my_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, count)
    except socket.error, (errno, msg):
        if errno == 1:
            # Operation not permitted
            msg = msg + (
                " - Note that ICMP messages can only be sent from processes"
                " running as root."
            )
            raise socket.error(msg)
        raise  # raise the original error

    my_ID = os.getpid() & 0xFFFF

    timeSent = send_one_ping(my_socket, dest_addr, my_ID)
    delay, addr, is_final, reached = receive_one_ping(my_socket, my_ID, timeout, timeSent)

    my_socket.close()
    return delay, addr, is_final, reached


def verbose_ping(dest_addr, timeout=2, max_ttl=30):
    """
    Send >count< ping to >dest_addr< with the given >timeout< and display
    the result.
    """
    for ttl in range(1, max_ttl):
        rtt = []
        try:
            delay, addr, is_final, reached = do_one(dest_addr, timeout, ttl)
        except socket.gaierror, e:
            print ("failed. (socket error: '%s')" % e[1])
            break
        if delay is None:
            print ("failed. (timeout within %ssec.)" % timeout)
        else:
            if reached:
                delay = delay * 1000
                print ("".join(["#", str(ttl), " -> (", str(addr[0]), ") ", str(delay), "ms"]))
            else:
                print ("".join(["#", str(ttl), " -> (*) ***"]))
        if is_final:
            break
    print


if __name__ == '__main__':
    verbose_ping("ufla.br")
