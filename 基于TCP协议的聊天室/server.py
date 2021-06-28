from socket import *
import threading
import time


def tcplink(sock, addr, sock_l):

    print('新客户端链接进来:', addr)
    sock.send('Welcome!'.encode('utf-8'))
    while True:
        try:
            data = sock.recv(1024)  # 接收
        except:continue
        # 用with操作文件，默认会关闭文件，不需要调用close()
        with open('[聊天记录文件].txt', 'a', encoding='utf-8') as f:
            # 写入接收到的数据
            f.write(time.time())
            f.write(data.decode('utf-8') + '\n')
        if data == 'byby':
            sock.close()
            break
        try:
        # 用新的套接字发送给解堵塞的所有ip
            for i in sock_l:
                i.sendto(data, addr)
        except:continue


if __name__ == '__main__':
    # 创建套接字
    s = socket(AF_INET,SOCK_STREAM)
    # 监听端口
    s.bind(('127.0.0.1',8086))
    # 等待连接
    s.listen(5)
    print('服务器初始化完毕，等待连接......')
    sock_l = list()
    while True:
        try:
            # 尝试接收一个新的连接
            sock, addr = s.accept()  # 起到一个主机的作用
            # 将新的套接字存放在列表里面
        except:continue
        if addr not in sock_l:
            sock_l.append(sock)
        # 创建新的线程来处理连接
        t = threading.Thread(target=tcplink, args=(sock, addr, sock_l))
        t.start()
