from socket import *
import threading
'''
客户端1
'''

client_sock = socket(AF_INET,SOCK_STREAM)
client_sock.bind(('127.0.0.1', 8087))
client_sock.connect(('127.0.0.1',8086))

def sendd():
        msg = input('>>>:')
        client_sock.send('client1:%s'.encode() % msg.encode('utf-8'))
        if msg == 'byby':
            client_sock.close()


if __name__ == '__main__':

    while True:
        try:
            b = client_sock.recv(1024)
            print(b.decode('utf-8'))
        except:
            print('服务器已关闭...')
            break
        t = threading.Thread(target=sendd)
        t.start()

client_sock.close()