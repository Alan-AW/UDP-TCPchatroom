from socket import *
import time, threading, re


# 下线判断
def break_out(send_msg):
    if send_msg:
        say = input('''
                       是否退出群聊？
                  “回车”确认--任意键取消:
                ''')
        if not say:
            return True

# 循环发送消息
def send_to(name):
    while True:
        send_msg = input('>>>:')
        # 避免报错
        if not send_msg:continue
        else:
            # 正则过滤敏感词
            ret = re.subn('[逼操傻日]','*', send_msg)
        # 发送给服务器进行广播到“群”
        send_for = name + ':' + ret[0]
        client_sock.sendto(send_for.encode('utf-8'), connect)
        # 输入内容检测是否下线
        if send_msg == '拜拜' or send_msg == 'bye':
            # 启动下线判断
            break_ou = break_out(send_msg)
            # 确认下线
            if break_ou:
                print('你已退出群聊...')
                # 进行广播本机下线
                exit_client = ('（系统通知:漂亮的【%s】已经退出群聊）\n' % name)
                client_sock.sendto(str(exit_client).encode('utf-8'), connect)
                # 关闭套接字
                client_sock.close()
                break
            else:
                continue

if __name__ == '__main__':
    # 生成套接字
    client_sock = socket(AF_INET, SOCK_DGRAM)
    # 一定要绑定自己的端口，否则服务器接收到随机的端口发不过来
    ip_port = ('127.0.0.1', 7789)
    client_sock.bind(ip_port)
    # 连接到服务器
    connect = ('127.0.0.1', 7788)
    # 欢迎语
    print('正在连接服务器...')
    time.sleep(1)
    print('欢迎进入“饭醉团伙”聊天室，新来的成员跟大家打个招呼吧！')
    name = input('请输入群备注:')


    t1 = threading.Thread(target=send_to, args=(name,))
    t1.start()
    while True:
        # 避免前面发送消息的时候关闭套接字，所以要踹
        try:
            # 尝试用本机套接字接收消息
            receve_msg = client_sock.recvfrom(1024)
            print(receve_msg[0].decode('utf-8'))
            # 报错肯定是前面关闭了套接字，退出，不接收消息
        except:break


