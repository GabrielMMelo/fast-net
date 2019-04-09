#!/usr/bin/env python

import socket
import time
import os

tcp_ip = '127.0.0.1'
tcp_port = 5006

s = socket.socket(socket.AF_INET,
				socket.SOCK_STREAM)
s.connect((tcp_ip, tcp_port))
#conn, addr = s.accept()
# def calc_upload():
# 	arquivo =  open('testando.txt','rb')
# 	print("entrei")
# 	tempo_inicial = time.time()
# 	print("Contando o tempo")
# 	pedaco_arquivo = arquivo.read(1024)
# 	print("li pedaco arquivo")
# 	while(pedaco_arquivo):
# 		s.send(pedaco_arquivo)
# 		print(pedaco_arquivo.decode())
# 		pedaco_arquivo = arquivo.read(1024)
# 	print("Sai do while")
# 	tempo_final = time.time()
# 	conn.send(str.encode("Ok"))
	
# 	arquivo.close()	
# 	tamanho_arquivo_bits = (os.path.getsize('testando.txt'))/(1024*1024*8)
# 	("Velocidade de Upload: " , tamanho_arquivo_bits/ (tempo_final-tempo_inicial))

def download():
	s.send(str.encode('requisitando'))
	arquivo = open('testando.txt','rb')
	tempo_inicial = time.time()
	pedaco_arquivo = s.recv(1024)
	while(pedaco_arquivo):
		#arquivo.write(pedaco_arquivo)
		pedaco_arquivo = s.recv(1024)
		if "Ok" in pedaco_arquivo.decode():
			print (pedaco_arquivo.decode())
			break
	tempo_final = time.time()
	arquivo.close()
	#print(tempo_inicial)
	#print(tempo_final)
	
	tamanho_arquivo_bits = (os.path.getsize('testando.txt'))/(1024*1024)
	#print(os.path.getsize('testando.txt'))
	#print(tamanho_arquivo_bits)
	print (tempo_final-tempo_inicial)
	print ("Velocidade de download :",  tamanho_arquivo_bits/(tempo_final-tempo_inicial), "Mbs")
	


while True:
	
	download()

	#calc_upload()

	data = s.recv(1024)
	if not data:
		break
	

s.close()
