#!/usr/bin/env python

import socket
import time
import os

tcp_ip = 'melodev.com.br'
tcp_port = 5006

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((tcp_ip, tcp_port))
# conn, addr = s.accept()


def calc_upload():
    arquivo = open('testando.txt', 'rb')

    pedaco_arquivo = arquivo.read(1024)
    while(pedaco_arquivo):
        s.send(pedaco_arquivo)
        pedaco_arquivo = arquivo.read(1024)
    tempo_final = time.time()
    arquivo.close()
    tamanho_arquivo_bits = (os.stat('testando.txt').st_size)/131072
    return tamanho_arquivo_bits / (tempo_inicial - tempo_final)


def download():
    tempo_inicial = time.time()
    s.send(str.encode('requisitando'))
    pedaco_arquivo = s.recv(1024)
    while(pedaco_arquivo):
        # arquivo.write(pedaco_arquivo)
        pedaco_arquivo = s.recv(1024)
        if "Ok" in pedaco_arquivo.decode():
            print (pedaco_arquivo.decode())
            break
    tempo_final = time.time()
    # arquivo.close()
    tamanho_arquivo_bits = (os.path.getsize('testando.txt')) / (1024 * 1024 * 8)
    print ("Velocidade de download :",  tamanho_arquivo_bits / (tempo_final-tempo_inicial), "Mbs")


while True:
    download()
    data = s.recv(1024)
    # calc_upload()
    if not data:
        break


s.close()
