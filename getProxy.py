import json
import random
import re
import threading
import time

import requests

# 抓取代理IP


lock = threading.Lock()  # 建立一个锁


# 验证代理IP有效性的方法
def proxycheck(i):
    # url = "http://opm.tangdi.net/tdopm/auth/loginView.do"  #打算爬取的网址
    try:
        # proxy_support = urllib.request.ProxyHandler({"http" : 'http://'+i})
        # opener = urllib.request.build_opener(proxy_support)
        # opener.addheaders=[("User-Agent","Mozilla/5.0 (Windows NT 10.0; WOW64)")]
        # urllib.request.install_opener(opener)
        # res = urllib.request.urlopen(url).read()
        requests.get("http://w2.aqu1024.club/pw/", proxies={"http": 'http://' + i})
        lock.acquire()  # 获得锁
        print(i, 'is OK')
        checkedProxyList.append(i)  # 写入该代理IP
        lock.release()  # 释放锁
    except Exception as e:
        lock.acquire()
        print(i, e)
        lock.release()


# 单线程验证
'''for i in range(len(proxys)):
    test(i)'''


def multithreadscheck():
    # 多线程验证
    threads = []
    for i in (rawProxyList):
        thread = threading.Thread(target=proxycheck, args=[i])
        threads.append(thread)
        thread.start()
    # 阻塞主进程，等待所有子线程结束
    for thread in threads:
        thread.join()


def wfile():
    data = {'checkedProxyList': checkedProxyList}
    with open(fname, "w") as fw:
        json.dump(data, fw)

    # with open(fname, 'w') as  op:
    #     op.write('rawProxyList:' + '\n')
    #     for m in rawProxyList:
    #         op.write(m + '\n')
    #     op.write('checkedProxyList:' + '\n')
    #     for j in checkedProxyList:
    #         op.write(j + '\n')

if __name__=='__main__':
    rawProxyList = []
    checkedProxyList = []
    fname = 'data.txt'
    url = 'http://www.66ip.cn/areaindex_33/2.html'
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64)"}
    r = requests.get(url=url, headers=headers)
    r.encoding = 'gbk'
    content = r.text

    pattern = re.compile('<td>([\d.]*?)</td>')  # 截取<td>与</td>之间第一个数为数字的内容
    ip_totle = re.findall(pattern, str(content))
    time.sleep(random.choice(range(1, 3)))
    # 打印抓取内容
    print(len(ip_totle) / 2)
    print('代理IP地址', '\t', '端口', '\t')
    for i in range(0, len(ip_totle), 2):
        rawProxyList.append(ip_totle[i] + ':' + ip_totle[i + 1])
        print(ip_totle[i], '\t', ip_totle[i + 1], '\t')
    rawProxyList = list(set(rawProxyList))
    multithreadscheck()
    wfile()

    # for page in range(1, 20):
    #     if page == 1:
    #         newurl = url + 'index.html'
    #     else:
    #         newurl = url + str(page) + '.html'
    #     # html = gethtml(url,['185.209.20.124:8888'])
    #     html = gethtml2(url)
    #     print(html)
    #     dict = getdict2(html)
    #     print(u'完成第' + newurl + u'页')
