#!/usr/bin/env python

import socket
import time
import os

TCP_IP = '127.0.0.1'
TCP_PORT = 5006

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
 
conn, addr = s.accept()
#print 'Endereco de conexao: ', addr

def calc_download():
	arquivo =  open('testando.txt','rb')
	pedaco_arquivo = arquivo.read(1024)
	while(pedaco_arquivo):
		print("Iniciando Download")
		conn.send(pedaco_arquivo)
		pedaco_arquivo = arquivo.read(1024)
		print("Passei aqui")
	conn.send(str.encode("Ok"))
	arquivo.close()
def upload():
	tempo_inicial = time.time()
	pedaco_arquivo = s.recv(1024)
	while(pedaco_arquivo):
		#arquivo.write(pedaco_arquivo)
		pedaco_arquivo = conn.recv(1024)
		if "Ok" in pedaco_arquivo.decode():
			print (pedaco_arquivo.decode())
			break
	tempo_final = time.time()
	#arquivo.close()
	tamanho_arquivo_bits = (os.path.getsize('testando.txt'))/(1024*1024*8)
	print ("Velocidade de download :",  tamanho_arquivo_bits/ (tempo_final-tempo_inicial), "Mbs")
	
while True:
	data = conn.recv(1024)
	print ("Requisicao aceita")
	calc_download()
	upload()
	#Tamanho do buffer.

	#print ("Mensagem Recebida:", data)
	#message = data.upper()
	#conn.send(message)  # echo
	#velocidade_download = calc_download()
	#conn.send(velocidade_download)



conn.close()
