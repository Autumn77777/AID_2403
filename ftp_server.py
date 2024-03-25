from socket import *
import sys,os
import signal
import multiprocessing


sockfd = socket()
sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
sockfd.bind(("0.0.0.0", 9999))
sockfd.listen(5)
signal.signal(signal.SIGCHLD,signal.SIG_IGN)

def help_info():
    return ("命令行输入 'show' 查看文件库中内容"
            "\n命令行输入 'push + 文件名称' 上传文件"
            "\n命令行输入 'get + 文件名称' 获取文件")

def f_show():
    return  '\n'.join(os.listdir())

def f_get(filename):
    file = os.listdir()
    if filename in file:
        with open(filename,'rb') as f:
            return f.read()
    else:
        return b"is not exist"

def f_push(filename,data):
    with open(filename,'wb') as f:
        f.write(data)

def subp(c):
    c.send(help_info().encode())
    while True:
        data = c.recv(1024)
        type_ = data.decode().split(' ')[0]
        if type_ == 'show':
            c.send(f_show().encode())
        elif type_ == 'get':
            filename = data.decode().split(' ')[1]
            print(filename)
            re = f_get(filename)
            print("re = ",re)
            c.send(re)
        elif data == 'push':
            filename = data.decode().split(' ')[1]
            # if filename in os.listdir():
            #     c.send("%s exist"%filename.encode())
            # else:
            data = c.recv(1024)
            f_push(filename,data)
        else:
            c.send(b'xxx')
while True:
    print("Wating connect...")
    try:
        connfd, addr = sockfd.accept()
        print("Connect from", addr)
    except KeyboardInterrupt:
        sys.exit("退出服务器")
    except Exception as e :
        print(e)
        continue
    t = multiprocessing.Process(target = subp,args=(connfd,))
    t.daemon = True  # 父进程结束则所有服务终止
    t.start()
