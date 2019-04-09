#!/usr/bin/env python

import socket

TCP_IP = '0.0.0.0'
TCP_PORT = 5006

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()

while True:
    data = conn.recv(1024)
    print ("Requisicao aceita")
    arquivo = open('testando.txt', 'rb')
    pedaco_arquivo = arquivo.read(1024)
    while(pedaco_arquivo):
        conn.send(pedaco_arquivo)
        pedaco_arquivo = arquivo.read(1024)
    conn.send(str.encode("Ok"))
    arquivo.close()

conn.close()
