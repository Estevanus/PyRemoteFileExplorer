'''
--------------------- credits ---------------------
this script is coding by G. E. Oscar Toreh
---------------------------------------------------
'''

import server as serv
import os
import sys
import time

s = serv.s
s.listen()

buff = 1024
mode = ["print", "write", "list"]
conList = []

def getDir(arg = None):
	return os.listdir(arg)

class cmdCollection:
	#collection of available command
	def __init__(self):
		pass
	def ls(self, arg):
		#get list of directory
		if arg == "":
			arg = None
		return getDir(arg), mode[0]
	def dir(self, arg):
		#get list of directory
		if arg == "":
			arg = None
		return getDir(arg), mode[0]
	def getcwd(self, arg):
		return os.getcwd(), mode[0]
	def chdir(self, arg):
		try:
			before = os.getcwd()
			print("changing director to " + arg)
			os.chdir(arg)
			after = os.getcwd()
			return "dir has changed from {0} into {1}".format(before, after), mode[0]
		except FileNotFoundError:
			return "Directory is not exist", mode[0]
		except:
			return "something is error", mode[0]
	def get(self, arg):
		if os.path.isfile(arg):
			f = open(arg, 'rb')
			data = f.read()
			f.close()
			return data, mode[1], arg
		else:
			return "File not found", mode[0]
	def help(self, arg):
		if arg == "":
			return help(cmdCollection), mode[0]
		else:
			if hasattr(cmdCollection, arg):
				fungsi = getattr(cmdCollection, arg)
				return help(fungsi), mode[0]
			else:
				print("command that you are refering is not avaiable")
				return "command that you are refering is not avaiable", mode[0]

def parseArg(kata):
	if " " in kata:
		h = kata.split(" ")
		cmd = h[0]
		arg = kata[len(cmd)+1:]
		return cmd, arg
	else:
		return kata, ""


print("starting the server...")
con, caddr = s.accept()
print("connected on : " + str(con))
def terima():
	cd = con.recv(buff)
	msg = cd.decode()
	#print(msg)
	cmd, arg = parseArg(msg)
	if cmd == "exit":
		return False
	else:
		if hasattr(cmdCollection, cmd):
			fungsi = getattr(cmdCollection, cmd)
			h = fungsi(cmdCollection, arg)
			x = h[0]
			m = h[1]
			filename = "none.txt"
			size = sys.getsizeof(x)
			if len(h) > 2:
				filename = h[2]
			print("sending mode " + m)
			con.send(m.encode())
			if type(x) == str:
				print("sending result of " + cmd)
				con.send(size.to_bytes(4, "big"))
				con.send(x.encode())
			elif type(x) == list and m == mode[2]:
				pa = len(x)
				print("number of list is " + str(pa))
				
				print("sending the number of list...")
				con.send(pa.to_bytes(4, "big"))
				
				print("sending the list...")
				for i in x:
					data = i.encode()
					con.send(sys.getsizeof(data).to_bytes(4, "big"))
					con.send(data)
			elif type(x) == bytes:
				print("sending name of file...")
				con.send(filename.encode())
				
				print("size of file is " + str(size))
				
				print("sending size data of file...")
				con.send(size.to_bytes(4, "big"))
				
				
				print("sending data...")
				con.send(x)
				print("done")
			else:
				xx = str(x)
				data = xx.encode()
				size = sys.getsizeof(data)
				con.send(size.to_bytes(4, "big"))
				con.send(data)
			
			print("data sent")
		else:
			print("command {0} not found".format(cmd))
			return "command that you are refering is not avaiable", mode[0]
		return True
	

while True:
	td = terima()
	if td == False:
		break

