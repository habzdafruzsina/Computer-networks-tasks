import socket, sys, select, threading

def findInArr(arr,id):
    for i in arr:
        if(i[0] == id):
            return i
    return None

def handleMess(data):
    mess_str = str(data,"UTF8")
    if("BE" in mess_str):
        arr = mess_str.split('|')
        item = [arr[1],arr[2],arr[3],arr[4]]
        files.append(item)
        t = threading.Timer(int(arr[2]),removeFromList,[item])
        t.start()
        return bytes("OK","UTF8")

    elif("KI" in mess_str):
        arr = mess_str.split('|')
        item = findInArr(files,arr[1])
        if(item != None):
            files.remove(item)
            return bytes(item[2] + "|" + item[3],"UTF8")
        else:
            return bytes("0|","UTF8")

def removeFromList(i):
    if i in files:
        files.remove(i)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = (sys.argv[1],int(sys.argv[2]))
sock.bind(server_address)

sock.listen()

inputs = [sock]

files = []

while(True):
    readable, writable, exceptional = select.select(inputs,[], inputs)

    for s in readable:
        if s is sock:
            connection, client_address = sock.accept()
            inputs.append(connection)
        else:
            data = s.recv(100)
            back_mess = handleMess(data)
            s.sendall(back_mess)
            inputs.remove(s)
            s.close()
