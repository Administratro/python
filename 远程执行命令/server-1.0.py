#coding:utf8

import socket
import subprocess
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
server.bind(('0.0.0.0',9999))
server.listen(5)
print('server runing...')
while True:
    #accept去listen半连接池中拿客户端请求对象
    conn,addr = server.accept()
    print(f'客户端的ip和port——>{addr}')
    while True:
        '''
        处理从半连接池拿的请求
        '''
        #在windows中如果突然关闭客户端，服务端会抛一个异常这个我们来捕获这个异常。
        try:
            cmd = conn.recv(1024)
        except:
            break
        #在linux和mac上，如果客户端发空字符，就说明连接断开
        if  not cmd:
            break

        #执行命令
        cmd_obj = subprocess.Popen(cmd.decode('gbk'),
                   shell=True,
                   stdout=subprocess.PIPE,
                   stderr=subprocess.PIPE
                   )
        out_res = cmd_obj.stdout.read()
        err_res = cmd_obj.stderr.read()
        #print(len(out_res),len(err_res))
        data_size = len(out_res) + len(err_res)
        #把数据总长度传给客户端（使用zfill方法，把数据总长度转成8个字节的二进制格式头信息，这样客户端先解析头信息就拿数据总长度）
        header=bytes(str(data_size),'utf-8').zfill(8)
        print('header:',header)
        conn.send(header)
        conn.send(out_res)
        conn.send(err_res)
    conn.close()#里的循环break后我们就关闭当前处理的请求连接。
        #当前请求关闭后服务下一个客户