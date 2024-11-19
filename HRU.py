import requests
from random import randint
from re import findall
from threading import Thread
import argparse
import sys

class Hru:
    result = []
    def __init__(self):
        pass

    ua_list = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.137 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:130.0) Gecko/20010101 Firefox/130.0",
        "Mozilla/5.0 (Windows NT 6.3; rv:132.0) Gecko/20100101 Firefox/132.0",
        "Mozilla/5.0 (Windows NT 6.3; Win64; rv:130.0) Gecko/20100101 Firefox/130.0",
        "Mozilla/5.0 (Windows NT 6.2; WOW64; x64; rv:132.0) Gecko/20010101 Firefox/132.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:131.0) Gecko/20100101 Firefox/131.0",
        "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.70 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.127 Mobile Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.59 Safari/537.36"
    ]

    def sendReq(self, url):
        headers = {
            'User-Agent': self.ua_list[randint(0, len(self.ua_list) - 1)],
            "Referer": url,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "DNT": "1",
            "Sec-GPC": "1",
        }
        try:
            ans = requests.get(url=url, headers=headers, timeout=2)
        except:
            return False
        try:
            ans.encoding = ans.apparent_encoding
            title = findall("<title>(.*?)</title>", ans.text)[0].strip()
        except IndexError:
            title = ""
        self.result.append([url, title, ans.status_code, len(ans.text)])

    def hruTodayFromFile(self, path):
        threads = []
        r = open(path, "r")
        while True:
            line = r.readline().strip()
            if line:
                threads.append(Thread(target=self.sendReq, args=(line,)))
            else:
                break
        r.close()
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        return self

    def hruTodayFromPipe(self, stream):
        threads = []
        urls = stream.split("\n")
        for url in urls:
            url = url.strip()
            threads.append(Thread(target=self.sendReq, args=(url,)))
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        return self

    def show(self):
        for item in self.result:
            print(f"{item[0]} 【{item[1]}】 【{item[2]}】 len: {item[3]}")

    def saveAsFile(self, path):
        with open(path, "w", encoding="utf-8") as f:
            for item in self.result:
                f.write(f"{item[0]} 【{item[1]}】 【{item[2]}】 len: {item[3]}\n")


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description="Thanks for using HRU.py, if there is any problem please contact me: 【Wechat: A2Cai_】 or 【Email: 1149652550@qq.com】")
    parser.add_argument("-f", "--file", help='files for detect')
    parser.add_argument("-s", "--show", help='display result on console', action="store_true")
    parser.add_argument("-o", "--output-file", help='filename for output')
    parser.add_argument("-p", "--pipe", help='receive target urls by pipe', action="store_true")
    args = parser.parse_args()
    file = args.file
    output_file = args.output_file
    is_show = args.show
    is_pipe = args.pipe
    # 必须需要传递参数 file 或 pipe
    if not file and not is_pipe:
        exit("Missing Param: -f or -p")
    # 通过管道获取标准输入
    if is_pipe and not file:
        hru = Hru()
        hru.hruTodayFromPipe(sys.stdin.read())
        if is_show and not output_file:
            hru.show()
        else:
            hru.saveAsFile(output_file)
    # 通过读取文件获取所有URL
    else:
        hru = Hru()
        hru.hruTodayFromFile(file)
        if is_show and not output_file:
            hru.show()
        else:
            hru.saveAsFile(output_file)