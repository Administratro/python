#coding:utf8
import socket
import subprocess
import os

def Cmd(cmd):
    """执行命令，并且把结果返回给主程序（命令执行成功和失败结果）"""
    if "cd" in cmd.decode('gbk'):
        #print(cmd.decode('gbk').split(' '))
        path=cmd.decode('gbk').split(' ')[1]
        os.chdir(path)
    else:
        pass
    
    cmd_obj = subprocess.Popen(cmd.decode('gbk'),
                   shell=True,
                   stdout=subprocess.PIPE,
                   stderr=subprocess.PIPE
                   )
    #print(cmd.decode('gbk'))
    out_res = cmd_obj.stdout.read()
    #print(cmd_obj)
    #print(out_res)
    err_res = cmd_obj.stderr.read()
    data_size = len(out_res) + len(err_res)
    return (out_res,err_res,data_size)

def Send_Data(conn,out_res,err_res,data_size):
    #把数据总长度传给客户端（使用zfill方法，把数据总长度转成8个字节的二进制格式头信息，这样客户端先解析头信息就拿数据总长度）
    header=bytes(str(data_size),'utf-8').zfill(8)
    print('header:',header)
    conn.send(header)
    conn.send(out_res)
    conn.send(err_res)
    
    
def login_Auth(conn):
    """1、首先发送Please login!字符串
       2、接收用户名和密码
       3、对比admin和密码是否正确，正确返回True否则返回Flase
    """
    
    try:
        conn.send('Please login!'.encode('utf-8'))
        username=conn.recv(1024)
        print(f"username:{username.decode('utf-8')}")
        password=conn.recv(1024)
        print(f"password:{password.decode('utf-8')}")
        
        if username.decode('utf-8')=="admin" and password.decode('utf-8') =="123456":
            return True
        else:
            return False
        
    except OSError:
        """当客户端用户在username输入框中Ctrl+C，那么就被捕获到这个异常"""

        print('111')
        print(f"Client {conn.getpeername()} disconnected during the process.")

        return False
        
    
def main():
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    server.bind(('0.0.0.0',9999))
    server.listen(5)
    print('server runing...')
    while True:
        #accept去listen半连接池中客户端请求，当有请求来时，才执行下面那个while循环。
        #如果没有请求那么一直在conn,addr = server.accept()这行代码上阻塞
        #不支持并发
        conn,addr = server.accept()
        print(f'客户端的ip和port——>{addr}')
        
        while True:
            try:
                if(login_Auth(conn)):
                    """
                    1、用户名和密码正确后，给客户端发送True
                    2、处理业务，也就是远程执行命令
                    3、把命令结果发送给客户端
                    """
                    conn.send(str(True).encode('utf-8'))
                    
                    while True:
                        '''
                        处理从半连接池拿的请求
                        '''
                        #在windows中如果突然关闭客户端，服务端会抛一个异常这个我们来捕获这个异常。
                        
                        try:
                            cmd_text = conn.recv(1024)
                        except:
                            break
                        #在linux和mac上，如果客户端发空字符，就说明连接断开
                        if  not cmd_text:
                            break

                        #执行命令
                        out_res,err_res,data_size=Cmd(cmd_text)
                        #把命令执行后的结果发送给客户端
                        Send_Data(conn,out_res,err_res,data_size)
                        
                    #当前请求关闭后服务下一个客户
                    #conn.close()
                    
                else:
                    #登陆失败发送False
                    conn.send(str(False).encode('utf-8'))
                    
                        
            except (OSError, ConnectionAbortedError, ConnectionResetError):
                """当客户端用户在username输入框中Ctrl+C，那么就被捕获到这个异常"""
                print('222')
                print(f"Client {addr} disconnected during the process.")
                conn.close()
                break
                    
            
                
           
            
if __name__ == "__main__":
    main()
