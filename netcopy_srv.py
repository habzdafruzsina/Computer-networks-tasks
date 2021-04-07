import socket, sys, hashlib

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

#netcopy server

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = (sys.argv[1],int(sys.argv[2]))
sock.bind(server_address)

sock.listen()

connection, client_address = sock.accept()

c = ' '

f = open(sys.argv[6],"w")
while(c != ''):
    c = str(connection.recv(100),"UTF8")
    f.write(c)
    
sock.close()

sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = (sys.argv[3],int(sys.argv[4]))
sock2.connect(server_address)

sock2.sendall(bytes("KI|" + sys.argv[5],"UTF8"))
reply = str(sock2.recv(100),"UTF8")
sock2.close()
reply_arr = reply.split('|')

if(reply_arr[1] == md5(sys.argv[6])):
    print("CSUM OK")
else:
    print("CSUM CORRUPTED")
