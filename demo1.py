import requests
import concurrent.futures


def vote():
    headers={
    'Accept':'text/plain, */*; q=0.01',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'en,zh-CN;q=0.9,zh;q=0.8',
    'Cache-Control':'no-cache',
    'Connection':'keep-alive',
    'Content-Type':'application/x-www-form-urlencoded',
    'Cookie':'22lF_e225_saltkey=O9992499; 22lF_e225_lastvisit=1575354060; 22lF_e225_sendmail=1; Hm_lvt_77e6328829d243222ff758d79882627e=1575357836; Hm_lpvt_77e6328829d243222ff758d79882627e=1575357836; 22lF_e225_lastact=1575357897%09plugin.php%09',
    'Host':'bbs.fanruan.com',
    'Origin':'http://bbs.fanruan.com',
    'Pragma':'no-cache',
    'Referer':'http://bbs.fanruan.com/dreamer/list/search/33',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
    'X-Requested-With':'XMLHttpRequest',
    }


    params={
    'id':'votes:vote',
    'act':'poll',
    'appid':'116',
    'formhash':'ba608150',
    }

    data={
    'referer':'http://bbs.fanruan.com/dreamer/list/search/33',
    'formhash':'ba608150',
    'handlekey':'dmo_vots',
    'sechash':'',
    'seccodeverify':''
    }

    proxies={
    'http':'http://127.0.0.1:1081/',
    'https':'https://127.0.0.1:1081/',
    }

    r=requests.post('http://bbs.fanruan.com/plugin.php',
    params=params,data=data,headers=headers)
    print(r.text)



with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(vote) for i in range(1000)]
    for future  in  concurrent.futures.as_completed(futures):
        pass
