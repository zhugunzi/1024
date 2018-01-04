import multiprocessing
import os
import random
import re
import time
import wsgiref.headers

import bs4
import requests

ProxyList = ["120.204.85.29:3128", "211.161.103.151:808"]
targetPath = "D:\\1024\\"
count_time = 0
UserAgent_List = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]


def get_request_headers():
    request_headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Upgrade-Insecure-Requests': '1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        # 'Cookie': ' __cfduid=d343dad4a395b45b4a0147d7779464e831508088915; a4184_pages=3; a4184_times=5; __tins__18654184=%7B%22sid%22%3A%201514458119221%2C%20%22vd%22%3A%203%2C%20%22expires%22%3A%201514460409125%7D; __51cke__=; __51laig__=3',
    }
    return request_headers

def findStr(string, subStr, findCnt):
    listStr = string.split(subStr,findCnt)
    if len(listStr) <= findCnt:
        return -1
    return len(string)-len(listStr[-1])-len(subStr)
def get_image_header():
    request_headers = {
        'User-Agent': random.choice(ProxyList),
    }
    return request_headers


theader = {
    'Connection': 'keep-alive',
    'Content-Length': '36',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    # 'Cookie':'__cfduid=d1e44c3b867674a1b5717aacc281fa1b21509814575; a4184_pages=1; a4184_times=2; __tins__18654184=%7B%22sid%22%3A%201514352610671%2C%20%22vd%22%3A%201%2C%20%22expires%22%3A%201514354410671%7D; __51cke__=; __51laig__=1',
    # 'User-Agent': random.choice(ProxyList),
}


def get_random_IP():
    return random.choice(UserAgent_List)


def IP_Test(ip, url_test, set_timeout=1):  # 测试IP地址是否可用,时间为3秒
    try:
        requests.get(url_test, headers=wsgiref.headers, proxies={'http': ip}, timeout=set_timeout)
        return True
    except:
        return False


def get_IP_test(num_IP=10):
    ip_url = 'http://www.youdaili.net/Daili/http/19733.html'  # 获取IP的网站
    test_url = 'http://t3.9laik.live/pw/'  # 测试IP是否可用的的网站
    wb_date = requests.get(ip_url, headers=wsgiref.headers)
    wb_date.encoding = 'utf-8'
    soup = bs4.BeautifulSoup(wb_date.text, 'lxml')
    ip = soup.select('div.arc > div.content > p > span')
    ip_list = []
    for i in ip:
        span_ip = i.get_text().encode('utf-8').split('@')[0]
        print(span_ip)
        if IP_Test(span_ip, test_url):  # 测试通过
            ip_list.append(span_ip)
            print('测试通过，IP地址为' + str(span_ip))
        if len(ip_list) > num_IP - 1:  # 搜集够N个IP地址就行了
            print('搜集到' + str(len(ip_list)) + '个合格的IP地址')
            return ip_list
    return ip_list


def get_1024_links(page):
    url = 'http://s2.lulujjs.info/pw/thread.php?fid=3&page={}'.format(page)
    url1 = 'http://s2.lulujjs.info/pw/'
    wb_data = requests.get(url)
    wb_data.encoding = 'utf-8'  # 不然会乱码，老司机探过这个雷
    # print wb_data.text
    soup = bs4.BeautifulSoup(wb_data.text, 'lxml')  # 我习惯用lxml
    links = soup.select('tr.tr3 > td > h3 > a')
    links_1024 = []
    for link in links:
        url = url1 + link.get('href')  # 拼接成帖子的链接
        links_1024.append(url)
    return links_1024[5:]  # 返回这一页50个帖子的链接列表


def get_format_filename(input_filename):  # 文件夹的名字不能含有的特殊符号，windows下的限定
    str_pattern = re.compile(r'[^\w\u4e00-\u9fa5]')
    input_filename = str_pattern.sub("", input_filename)
    # for s in ['?', '*', '<', '>', '\★', '！', ':', '/']:
    #     while s in input_filename:
    #         input_filename = input_filename.strip().replace(s, '')
    return input_filename


def download_single_image(image_url, proxy_flag=False, try_time=0):  # 首先尝试直接下载，一次不成功则尝试使用代理
    if not proxy_flag:  # 不使用代理
        try:
            image_html = requests.get(image_url, headers=get_image_header(), timeout=60)
            print('图片直接下载成功')
            time.sleep(1)
            return image_html  # 一次就成功下载！
        except:
            return download_single_image(image_url, proxy_flag=True)  # 否则调用自己，使用3次IP代理
    else:  # 使用代理时
        if try_time < count_time:
            try:
                print('尝试第' + str(try_time + 1) + '次使用代理下载')
                # IP_address=get_random_IP()[0]
                image_html = requests.get(image_url, headers=get_image_header(),
                                          proxies={'http': 'http://' + get_random_IP()}, timeout=20)
                print('状态码为' + str(image_html.status_code))
                if image_html.status_code == 200:
                    print('图片通过IP代理处理成功！')
                    return image_html  # 代理成功下载！
                else:
                    a = download_single_image(image_url, proxy_flag=True, try_time=(try_time + 1))
                    return a
            except:
                print('IP代理下载失败')
                a = download_single_image(image_url, proxy_flag=True, try_time=(try_time + 1))  # 否则调用自己，使用3次IP代理
                return a
        else:
            print('图片未能下载' + image_url)
            return None


def download_single_torrent(torrent_url, data, proxy_flag=False, try_time=0):  # 首先尝试直接下载，一次不成功则尝试使用代理
    if not proxy_flag:  # 不使用代理
        try:
            torrent = requests.post(torrent_url, headers=theader, data=data, timeout=60)
            print('torrent直接下载成功'+data['name'])
            time.sleep(1)
            return torrent  # 一次就成功下载！
        except:
            return download_single_torrent(torrent_url, data=data, proxy_flag=True)  # 否则调用自己，使用3次IP代理
    else:  # 使用代理时
        if try_time < count_time:
            try:
                print('尝试第' + str(try_time + 1) + '次使用代理下载')
                # IP_address=get_random_IP()[0]
                torrent = requests.post(torrent_url, data=data, headers=theader,
                                        proxies={'http': 'http://' + get_random_IP()}, timeout=20)
                print('状态码为' + str(torrent.status_code))
                if torrent.status_code == 200:
                    print('torrent通过IP代理处理成功！')
                    return torrent  # 代理成功下载！
                else:
                    torrent = download_single_torrent(torrent_url, data=data, proxy_flag=True, try_time=(try_time + 1))
                    return torrent
            except:
                print('IP代理下载失败')
                torrent = download_single_torrent(torrent_url, data=data, proxy_flag=True,
                                                  try_time=(try_time + 1))  # 否则调用自己，使用3次IP代理
                return torrent
        else:
            print('torrent未能下载' + data['name'])
            return None


def get_torrent(torrent_link, filepath):
    host=torrent_link[:findStr( torrent_link,'/',3 )]
    torrent_download_url =host+'/updowm/down.php'
    # s = requests.Session()
    # wb_date = s.get(torrent_link, headers=get_request_headers())
    wb_date = requests.get(torrent_link, headers=get_request_headers())
    wb_date.encoding = 'utf-8'
    soup = bs4.BeautifulSoup(wb_date.text, 'lxml')
    data = {}
    for i in soup.select('form input'):
        if i.get('name'):
            data[i.get('name')] = i.get('value')
            # print data
    theader['Host'] = host
    theader['Referer'] = torrent_link
    torrent = download_single_torrent(torrent_download_url, data=data)
    if (torrent == None):
        return
    with open(filepath + '.torrent', 'wb+') as f:
        f.write(torrent.content)




def get_1024_details(url):  # 这里接收get_1024_links返回的link链接列表
    wb_date = requests.get(url)
    wb_date.encoding = 'utf-8'
    soup = bs4.BeautifulSoup(wb_date.text, 'lxml')
    # print '子页面读取完毕，开始尝试处理图片'
    # with open(os.getcwd() + '//'+filename+'//' +filename + '.jpg', 'wb') as f:
    try:
        path_name = soup.select('#subject_tpc')[0].get_text()
        save_dir = os.path.join(targetPath,get_format_filename(path_name))

        if not os.path.exists(save_dir):  # windows保存文件的坑，不然乱码
            os.makedirs(save_dir)
        # 下载文件
        torrent_link=''
        pic_link=''
        a_tags=soup.select('#read_tpc > a')
        for aTag in a_tags:
            try:
                # 下载torrent
                torrent_link = aTag.get('href')
                if str(torrent_link).endswith('html')==False:
                    continue
                # soup.select('#read_tpc > a')[0].find_previous_sibling("img").get('src')
                # 获取torrent 前一张图片的名称  查找兄弟节点
                img_tag = aTag.find_previous_sibling("img")
                if img_tag != None:
                     first_pic_url=img_tag.get('src')
                     filename = first_pic_url[first_pic_url.rindex('/') + 1:first_pic_url.rindex('.')]
                else:
                    filename=torrent_link[torrent_link.rindex('/') + 1:torrent_link.rindex('.')]
                get_torrent(torrent_link, os.path.join(save_dir, filename))
            except Exception as e:
                print('下载toorrent出错'+torrent_link, e)  # 出错，返回出错链接跟异常
        for imgTag in soup.select('#read_tpc > img'):
            try:
                # 下载图片
                pic_link = imgTag.get('src')
                pic = download_single_image(pic_link)  # 用的是戴司机的download_single_image函数
                if(pic==None):
                    continue
                with open(os.path.join(save_dir, pic_link[pic_link.rindex('/') + 1:]), 'wb') as f:
                    f.write(pic.content)
            except Exception as e:
                print('下载img出错'+pic_link, e)  # 出错，返回出错链接跟异常
    except Exception as e:
        print(url, e)  # 出错，返回出错链接跟异常


if __name__ == '__main__':

    pool = multiprocessing.Pool(processes=7)
    for i in range(1, 2):
        print('正在爬起第' + str(i) + '页')
        links = get_1024_links(i)
        try:
            pool.map(get_1024_details, links)
        except IndexError:
            pass
    pool.close()
    pool.join()
