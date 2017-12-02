import socket, select, thread

addr = socket.gethostname()
port = 16047

inputs = []
fd = {}  # file descriptor
status = {}

'''
def Startthread(client, addr):
    print('Received new client connection. %s:%s' % (addr[0], addr[1]))

    th = HandlerThread(client)
    t = thread(target=th.handler)
    t.setDaemon(True)
    t.start()


class connectionThread(object):
    queue = []


    def __init__(self, client):
        self.client = client

    
'''

def online(fd, status):
    onlineList = []
    for client in fd:
        if status[client]:
            onlineList.append(fd[client])
    return onlineList


def start():
    print 'Server start'
    server = socket.socket()
    server.bind((addr, port))
    server.listen(5)

    return server


def newClient(server):
    client, add = server.accept()
    try:
        welcome = '''Welcome into the CHAT ROOM, 
                    please use these commands to chat: 
                    login, newuser, send, logout'''
        client.send(welcome)
        #print 'To ' + fd[client][0] + ' : ' + welcome
        inputs.append(client)
        fd[client] = add
        status[client] = False
    except Exception, e:
        print e


def run():
    server = start()
    inputs.append(server)

    while True:
        r, w, e = select.select(inputs, [], [])
        for temp in r:
            if temp is server:
                newClient(server)
            else:
                disconnect = False
                try:
                    data = temp.recv(1024)
                except socket.error:
                    data = fd[temp] + ' leave the room'
                    disconnect = True

                if disconnect:
                    inputs.remove(temp)
                    print data
                    for other in inputs:
                        if other != server and other != temp:
                            try:
                                other.send(data)
                                print 'To ' + fd[other] + ' : ' + data
                            except Exception, e:
                                print e
                    del fd[temp]

                else:
                    if isinstance(fd[temp], tuple):
                        print fd[temp][0] + ':' + data
                    else:
                        print fd[temp] + ':' + data
                    spliter = data.split(' ', 1)
                    if spliter[0] != '':
                        if spliter[1] != '':
                            switch[spliter[0]](spliter[1], temp)
                        else:
                            switch[spliter[0]](temp)

                    # logout don't have spliter[1]


def case1(data, client):
    # login
    userFile = open('users.txt')
    res = ''
    try:
        flag = 0
        spliter2 = data.split(' ', 1)
        acc = spliter2[0]
        pas = spliter2[1]
        for line in userFile:
            spliter = line.split(' ', 1)
            account = spliter[0]
            password = spliter[1][:-1]
            if account == acc:
                if password == pas:
                    res = 'Login success, these people are online: %s' % (online(fd, status))
                    fd[client] = account
                    status[client] = True
                    #client.send(res)
                    #print 'To ' + fd[client] + ' : ' + res
                    flag = 1
                else:
                    res = 'Wrong password'
                    flag = 1
        if flag == 0:
            res = 'No account'
    finally:
        client.send(res)
        a = fd[client];
        print 'To ' + fd[client] + ' : ' + res
        userFile.close()


def case2(data, client):
    # newuser
    userFile = open('users.txt', 'r+')
    try:
        flag = 0
        spliter2 = data.split(' ', 1)
        acc = spliter2[0]
        for line in userFile:
            spliter = line.split(' ', 1)
            account = spliter[0]
            if account == acc:
                flag = 1
    finally:
        if flag == 0:
            with open('users.txt', 'a') as file2:
                file2.write(data+'\n')
                file2.close()
            res = 'You made a new account, please login again'
        else:
            res = 'The account existed, please login or make another account'
        userFile.close()
        client.send(res)
        print 'To ' + fd[client][0] + ' : ' + res


def case3(data, client):
    # send
    if not status[client]:
        res = 'You need to login to chat with others'
        client.send(res)
    else:
        for other in inputs:
            if other != client:
                try:
                    other.send(fd[client] + ' say: ' + data)
                    print 'To ' + fd[client] + ' : ' + fd[client] + ' say: ' + data
                except Exception, e:
                    print e


def case4(client):
    # logout
    if not status[client]:
        res = 'You didn\'t login'
        client.send(res)
        print 'To ' + fd[client] + ' : ' + res
    else:
        res = 'You logout'
        client.send(res)
        print 'To ' + fd[client] + ' : ' + res
        del fd[client]
        del status[client]
        inputs.remove(client)
        client.shutdown()
        client.close()


switch = {'login': case1,
          'newuser': case2,
          'send': case3,
          'logout': case4}

if __name__ == '__main__':
    run()
