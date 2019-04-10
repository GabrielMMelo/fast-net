from __future__ import print_function
import ping
import socket


class Traceroute:
    def __init__(self, dest_addr, timeout=2, max_ttl=30, counts=4):
        self.ping = ping.Ping()
        self.dest_addr = dest_addr
        self.timeout = timeout
        self.max_ttl = max_ttl
        self.counts = counts
        self.traceroute()

    def traceroute(self):
        # logica do traceroute
        for ttl in range(1, self.max_ttl):
            rtt = []
            address = "?"
            for counter in range(1, self.counts):
                try:
                    delay, addr, is_final, reached = self.ping.prepare_ping(self.dest_addr, self.timeout, ttl)
                    if not addr[0] == "*":  # se nao ocorreu timeout
                        address = addr[0]
                    rtt.append(delay)
                except socket.gaierror as e:
                    print ("failed. (socket error: '%s')" % e[1])
                    break

            print ("".join(["#", str(ttl), " -> (", address, ") "]), *rtt)

            if is_final:  # chegou ao destino final
                break


if __name__ == '__main__':
    Traceroute("netvasco.com.br")
