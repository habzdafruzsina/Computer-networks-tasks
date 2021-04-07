import socket
import struct

unpacker = struct.Struct('l 1000s')
packer = struct.Struct('l')
connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

actual_offset = None

server_address = ('localhost', 10000)

connection.sendto(packer.pack(1), server_address)

while(True):

	result, server_addr = connection.recvfrom(10000)
	unpacked_data = unpacker.unpack(result)
	
	if(unpacked_data[0] == -1):
		break
	
	if(actual_offset != unpacked_data[0]):
		data = unpacked_data[1].decode('utf-8')
		print(data)
		actual_offset = unpacked_data[0]
		
		
	packed_data = packer.pack(actual_offset)
	connection.sendto(packed_data, server_address)
	
connection.close()