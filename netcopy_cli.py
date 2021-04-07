import socket, sys, hashlib

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

#checksum server

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = (sys.argv[3],int(sys.argv[4]))
sock.connect(server_address)

checksum = md5(sys.argv[6])
packed = bytes("BE|" + sys.argv[5] + "|60|" + str(len(checksum)) + "|" + str(checksum) ,"UTF8")

sock.sendall(packed)

sock.close()

sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = (sys.argv[1],int(sys.argv[2]))
sock2.connect(server_address)

f = open(sys.argv[6],'r')

while True:
    line = f.readline()
    sock2.sendall(bytes(line,"UTF8"))
    if(line == ''): break



