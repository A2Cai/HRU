### Usage

python HRU.py [-h] [-f FILE] [-s] [-o OUTPUT_FILE] [-p]

Thanks for using HRU.py, if there is any problem please contact me: 【Wechat: A2Cai_】 or 【Email: 1149652550@qq.com】

1. Googlehack + asset survival detect

`python bingHack/bingHack.py -k "site:edu.cn" -n 100 -f | python HRU/HRU.py -p -s`

2. Display the results on the console

`python HRU.py -f test_urls.txt -s`

3. Save the results as a file

`python HRU.py -f test_urls.txt -o result.txt`

### Options

`-h, --help`	show this help message and exit

`-f FILE, --file FILE`	files for detect

`-s, --show` 	display result on console

`-o OUTPUT_FILE, --output-file OUTPUT_FILE`	filename for output

`-p, --pipe` 	receive target urls by pipe

### What is HRU?

> HRU is actually how are you, it's just that the object is not a person, but a web server. The function of HRU is the same as that of httpx, used for asset survival detection.