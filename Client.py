import socket, select, threading;

host = socket.gethostname()
port = 16047

def start():
    client = socket.socket()
    client.connect((host, port))
    return client

def receiveMessage(client):
    server = [client]
    while True:
        r, w, e = select.select(server, [], [])
        if client in r:
            try:
                print client.recv(1024)
            except socket.error:
                print 'Socket is error'
                exit()

def sendMessage(client):
    while True:
        try:
            message = raw_input()
        except Exception, e:
            print 'Cannot input'
            exit()
        try:
            client.send(message)
            if message == 'logout':
                exit()
        except Exception, e:
            print e
            exit()

if __name__ == '__main__':
    client = start()
    t = threading.Thread(target=receiveMessage, args=(client,))
    t.start()
    t1 = threading.Thread(target=sendMessage, args=(client,))
    t1.start()