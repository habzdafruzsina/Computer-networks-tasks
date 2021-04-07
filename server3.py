import socket
import struct
import sys

packer = struct.Struct('l 1000s')
unpacker = struct.Struct('l')
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

addr = ('localhost', 10000)
s.bind(addr)


buf = 1000


f = open("text.txt","rb")
data = f.read(buf)

offset = 0

firstrecdata, client_addr = s.recvfrom(16)

while(data):
	values = (offset*1000, data)
	packed_data = packer.pack(*values)
	
	recdata = None
	
	while (recdata == None):
		s.sendto(packed_data, client_addr)
		
		s.settimeout(5)
		recdata, client_addr = s.recvfrom(16)
		
	unpacked_data = unpacker.unpack(recdata)
	
	data = f.read(buf)
	offset = offset + 1

values = (-1, bytes("" ,"UTF8"))
packed_data = packer.pack(*values)        
s.sendto(packed_data, client_addr)		

s.close()
f.close()