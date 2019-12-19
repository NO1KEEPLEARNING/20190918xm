import requests
from bs4 import BeautifulSoup
cookies = {
    'bcolor': 'null',
    'font': 'null',
    'size': 'null',
    'color': 'null',
    'width': 'null',
    'clickbids': '18836',
    'Hm_lvt_30876ba2abc5f5253467ef639ca0ad48': '1571030311,1571030949,1571031218',
    'Hm_lpvt_30876ba2abc5f5253467ef639ca0ad48': '1571031588',
}

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

response = requests.get('https://www.biqu6.com/2_2583/', headers=headers, cookies=cookies)

print(response.text)
# class downloder(object):
#     def __init__(self):
#         self.server = 'http://www.biqukan.com'
#         self.target = 'http://www.biqukan.com/1_1094/'
#         self.names = []  #存放章节名字
#         self.urls = [] #存放章节链接
#         self.nums = 0 # 章节数量
#     def get_download_url(self):
#         req = requests.get('https://www.biqu6.com/2_2583/', headers=headers, cookies=cookies)
#
#         html = req.text
#         # print(html)
#         div_bf = BeautifulSoup(html)
#         div = div_bf.find_all('div',id='list')
#         a_bf = BeautifulSoup(str(div[0]))
#         a = a_bf.find_all('a')
#         for each in a:
#             self.names.append(each.string)
#             self.urls.append('https://www.biqu6.com/2_2583/'+each.get('href'))
#         self.nums = len(a)
#
#     def writer(self, name, path, text):
#         write_flag = True
#         with open(path, 'a', encoding='utf-8') as f:
#             f.write(name + '\n')
#             f.writelines(text)
#             f.writelines('\n\n')
#
#     def get_contents(self, target):
#         req = requests.get(url=target)
#         html = req.content
#         # print('html',html)
#         bf = BeautifulSoup(html)
#         texts = bf.find_all('div', id='content')
#
#         # texts=str(texts[0]).replace('<br/>','\n')
#         # print('texts',texts)
#         # texts = texts[0].text.replace('&nbsp', '\n\n')
#         # texts = texts[0].text.replace('<br/>', '\n\n')
#         # texts = texts[0].text.replace('<br/>', '\n\n')
#         # texts = texts[0].text.replace('<br>', '\n\n')
#
#         return texts
#
#
# if __name__ == '__main__':
#     dl = downloder()
#     dl.get_download_url()
#     # print(dl.urls)
#     print(dl.nums)
#     print('开始下载')
#     for i in range(dl.nums):
#         dl.writer(dl.names[i], '用点.txt', dl.get_contents(dl.urls[i]))
#         print('第'+str(i)+'章下载完')
#     print("下载完成")