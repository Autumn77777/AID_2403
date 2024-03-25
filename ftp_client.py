import sys,os
from socket import *
from time import sleep
ADDR = ('192.168.20.207',9999)
class FTPClient:
    # 客户端处理，查看，上传，下载，退出
    def __init__(self,sockfd):
        self.sockfd = sockfd
    def show(self):
        self.sockfd.send(b"L")
        data = self.sockfd.recv(4096)
        print(data.decode())
    def quit_(self):
        self.sockfd.send(b"Q")
        self.sockfd.close()
        sys.exit('退出客户端')
    def get_(self,cmd):
        try:
            filename = cmd.split()[1]
        except IndexError:
            return
        send_info = "G %s"%filename
        self.sockfd.send(send_info.encode())
        data = self.sockfd.recv(128)
        if data == b'OK':
            with open(filename,'wb') as f:
                while True:
                    get_data = self.sockfd.recv(1024)
                    if get_data == b"#end#":
                        break
                    f.write(get_data)
        elif data == b'No':
            print("'%s'文件不存在"%filename)
    def put_(self, cmd):
        try:
            filename = cmd.split()[1]
        except IndexError:
            return
        send_info = "P %s" % filename
        try:
            with open(filename,'rb') as f:
                self.sockfd.send(send_info.encode())
                data = self.sockfd.recv(128)
                if data == b'OK':
                    while True:
                        data = f.read(1024)
                        if not data:
                            sleep(0.1)
                            self.sockfd.send(b'#end#')
                            return
                        self.sockfd.send(data)
                elif data == b'No':
                    print("'%s'文件已存在" % filename)
        except Exception:
            print("本地没有'%s'文件" % filename)

def main():
    sockfd = socket()
    sockfd.connect(ADDR)
    client = FTPClient(sockfd)
    print("\n==================命令选项==================")
    print("*********      list    #查看文件库    *********")
    print("*********    get file   #获取文件     *********")
    print("*********    put file   #上传文件     *********")
    print("*********       quit      #退出      *********")
    print("======================================")
    while True:
        try:
            cmd = input("输入命令: ")
        except KeyboardInterrupt:
            cmd = 'quit'
        if cmd.strip() == 'list':
            client.show()
        elif cmd.strip() == 'quit':
            client.quit_()
        elif cmd.split(' ')[0] == 'get':
            client.get_(cmd)
        elif cmd.split(' ')[0] == 'put':
            client.put_(cmd)
        else:
            continue
if __name__ == '__main__':
    main()
