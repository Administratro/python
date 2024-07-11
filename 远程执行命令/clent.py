#coding:utf8
import socket

def recvData(clent):
    #拿到服务端发来的数据总长度,按规则先收这个头部信息，头部信息收到后再去收数据部分
    data_size = int(clent.recv(8).decode('utf-8'))
    recv_size = 0
    data = b''
    while data_size > recv_size:

        try:
            res = clent.recv(1024)
            data += res
            recv_size += len(res) 
        except:
            break
    #windows下使用gbk，linux下使用utf-8
    return data.decode('gbk','ignore')
    
def login(clent):
    """
    1、先收服务器端登陆字符串
    2、把用户名和密码发送到服务器端
    """
    try:
        da=clent.recv(1024)
        print(da.decode('utf-8'))
        username = input("username:").strip()
        clent.send(username.encode('utf-8'))
        password = input("password:").strip()
        clent.send(password.encode('utf-8'))
        
    except KeyboardInterrupt:
        print("\nClient stopped by keyboard interrupt.")
        clent.close()
        exit(0)

def main():
    cl = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    cl.connect(('127.0.0.1',9999))
    flag=False
    while True:
        login(cl)
        #登陆成功服务器发送True，失败则发送Flase
        flag=cl.recv(1024).decode('utf-8')
        if(flag=="True"):
            print("login secsseful")
            while True:
                cmd = input("@@@").strip()
                if not cmd:
                    continue
                    
                if cmd=="exit":
                    print("exit...")
                    exit(0)
                    
                #发送命令
                cl.send(cmd.encode('gbk'))
                #收数据
                Data=recvData(cl)
                #打印出结果
                print(Data)
                #break 注意这里不能break，不然后程序会在flag=cl.recv(1024).decode('utf-8')阻塞
        else:
            print("login failed")
    


if __name__=="__main__":
    main()