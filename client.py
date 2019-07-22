'''
--------------------- credits ---------------------
this script is coding by G. E. Oscar Toreh
---------------------------------------------------
'''

import socket
from socket import AF_INET, SOCK_STREAM
import multiprocessing as mp

buff = 1024
mode = ["print", "write", "list"]
s = socket.socket(AF_INET, SOCK_STREAM)

port = 8075

host = str(input("Masukan addressnya: "))
#print("\n")

addr = (host, port)

s.connect(addr)


psn = ""
while True:
	psn = str(input(">>"))
	if psn == "exit":
		s.close()
		break
	else:
		s.send(psn.encode())
		data = s.recv(buff)
		m = data.decode()
		#print("mode " + m)
		if m == mode[0]:
			szd = s.recv(buff)
			sz = int.from_bytes(szd, "big")
			
			loop = int(sz / buff)
			patok = sz - loop * buff
			if patok > 0:
				loop += 1
			
			data = b""
			for i in range(loop):
				data += s.recv(buff)
			print(data.decode())
		elif m == mode[1]:
			print("get name of file...")
			filename = s.recv(buff).decode()
			
			print("name of file is " + filename)
			
			print("get size of file...")
			fzd = s.recv(buff)
			
			fz = int.from_bytes(fzd, "big")
			print("size of file is " + str(fz) + " bytes")
			
			loop = int(fz / buff)
			patok = fz - loop * buff
			if patok > 0:
				loop += 1
		

			print("get and writing data into file...")
			f = open(filename, 'wb')
			j = 0
			for i in range(loop):
				data = s.recv(buff)
				f.write(data)
				if i / loop > j:
					j += 0.1
					print("file recieved {0} percents".format(str(j * 100)))
			f.close()
			print("done")
		elif m == mode[2]:
			jml = int.from_bytes(s.recv(buff), "big")
			print("number of list is " + str(jml))
			
			l = []
			for i in range(jml):
				szd = s.recv(buff)
				sz = int.from_bytes(szd, "big")
				
				loop = int(sz / buff)
				patok = sz - loop * buff
				if patok > 0:
					loop += 1
					
				data = b""
				for j in range(loop):
					data += s.recv(buff)
				l.append(data.decode())
				
			for i in l:
				print(i)