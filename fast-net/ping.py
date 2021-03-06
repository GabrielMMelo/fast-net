"""
based on github open project avaliable in  https://github.com/samuel/python-ping
"""

from __future__ import print_function
import os
import socket
import struct
import select
from time import time

from checksum import checksum

timer = time

ICMP_ECHO_REQUEST = 8


class Ping:
    def receive_ping(self, my_socket, ID, timeout, tempo_enviado):
        time_left = timeout
        while True:
            started_select = timer()
            selected = select.select([my_socket], [], [], time_left)  # aguarda I/O
            select_time = (timer() - started_select)
            if selected[0] == []:  # Timeout estourou
                return "*", "*", False, False

            tempo_recebido = timer()
            recPacket, addr = my_socket.recvfrom(567)  # tamanho maximo do ICMP
            icmpHeader = recPacket[20:28]
            type, code, checksum, packetID, sequence = struct.unpack(
                "bbHHh", icmpHeader
            )

            # converte para milissegundos
            delay = (tempo_recebido - tempo_enviado) * 1000

            # tempo excedido ICMP
            if type == 11:
                return delay, addr, False, True

            # sucesso
            elif type != 8 and packetID == ID:
                return delay, addr, True, True

            # desconta tempo no select
            time_left = time_left - select_time
            if time_left <= 0:
                return

    def send_ping(self, my_socket, dest_addr, ID):
        dest_addr = socket.gethostbyname(dest_addr)

        # Header possui type (8) | code (8) | checksum (16) | id (16) | sequence (16)
        my_checksum = 0

        # montagem de header provisorio e checksum 0
        header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, my_checksum, ID, 1)
        bytesInDouble = struct.calcsize("d")  # tamanho de double no so
        data = (192 - bytesInDouble) * "Q"

        # calcula checksum usando header provisorio
        my_checksum = checksum(header + data)

        # remonta o header com o checksum correto
        header = struct.pack(
            "bbHHh", ICMP_ECHO_REQUEST, 0, socket.htons(my_checksum), ID, 1
        )
        packet = header + data
        sent_time = timer()  # pega tempo
        my_socket.sendto(packet, (dest_addr, 80))
        return sent_time

    def prepare_ping(self, dest_addr, timeout, count):
        icmp = socket.getprotobyname("icmp")
        try:
            my_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
            my_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, count)
        except socket.error as e:
            if e.errno == 1:
                # operacao nao permitida
                msg = (
                    " - Mensagens por ICMP somente podem ser enviadas com permissoes root"
                )
                raise socket.error(msg)
            raise  # raise the original error

        my_ID = os.getpid() & 0xFFFF

        timeSent = self.send_ping(my_socket, dest_addr, my_ID)
        delay, addr, is_final, reached = self.receive_ping(my_socket, my_ID, timeout, timeSent)

        my_socket.close()
        return delay, addr, is_final, reached
