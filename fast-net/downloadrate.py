#!/usr/bin/env python

import socket
import time
import os


class DownloadRate:
    def __init__(self, tcp_ip="melodev.com.br", tcp_port=5006, file="../dist/dummy_file.txt"):
        self.tcp_ip = tcp_ip
        self.tcp_port = tcp_port
        self.file = file
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((tcp_ip, tcp_port))
        self.download()

    def receive_file(self):
        self.s.send(str.encode('requisitando'))
        tempo_inicial = time.time()
        pedaco_arquivo = self.s.recv(1024)

        while(pedaco_arquivo):
            pedaco_arquivo = self.s.recv(1024)
            if "Ok" in pedaco_arquivo.decode():
                print (pedaco_arquivo.decode())
                break
        tempo_final = time.time()

        tamanho_arquivo_bits = (os.path.getsize(os.path.dirname(__file__) + '/' + self.file))/(1024*1024)
        print "Tempo total gasto:", tempo_final-tempo_inicial, "s"
        print "Velocidade de download :",  tamanho_arquivo_bits/(tempo_final-tempo_inicial), "Mbs"

    def download(self):
        while True:
            self.receive_file()
            data = self.s.recv(1024)
            if not data:
                self.s.close()
                break
