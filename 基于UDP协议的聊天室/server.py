# 引入
from socket import *
import threading, time

if __name__ == '__main__':
    # 先定义空的ip池
    l_ip = []
    # 创建套接字
    server_sock = socket(AF_INET, SOCK_DGRAM)
    # 绑定端口
    ip_port = ('127.0.0.1', 7788)
    server_sock.bind(ip_port)
    # 服务器开启通知
    '''
    进度度条
    '''
    def show():
        names = 0
        while True:
            aa = (names / 100) * 100
            print('\r当前进度为%.2f %%' % aa, end='')
            names += 1
            time.sleep(0.01)
            if aa == 100:
                break
        print('链接成功！')
    show()
    print('The server is waiting for connection...')
    while True:
        # 接收（当客户端关闭套接字的时候会导致我服务器也被动关闭）
        try:  # 多以要踹
            receve_msg, receve_port = server_sock.recvfrom(1024)
        except:
            continue
        print('这是接收到的消息：' + receve_msg.decode('utf-8'))
        # 判断：如果收到数据，就创建文件。否则不创建
        if receve_msg:
            # 用with操作文件，默认会关闭文件，不需要调用close()
            with open('[聊天记录文件].txt', 'a', encoding='utf-8') as f:
                # 写入接收到的数据
                f.write(receve_msg.decode('utf-8') + '\n')
                # f.seek(-1)
                print('聊天记录已保存到本地...')
        # 写入IP池
        if receve_port not in l_ip:
            l_ip.append(receve_port)


    # 转发
def send_to(receve_msg, l_ip):
    for i in l_ip:
        server_sock.sendto(receve_msg, i)


    t = threading.Thread(target=send_to, args=(receve_msg, l_ip))
    t.start()

# 服务器不能关闭
# server_sock.close()
