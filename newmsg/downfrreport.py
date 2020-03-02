import requests
from multiprocessing import Pool
import time
import os
def donload(nums):
    for i in range(1,nums):
        if i<10:
            num ='0000'+str(i)
            print(num)
        elif  100>i>=10:
            num='000'+str(i)
            print(num)
        else:
            num ='00'+str(i)
            print(num)
        conn= requests.get('http://frcourse-video-out.oss-cn-shanghai.aliyuncs.com/Act-ss-m3u8-hd/8d91e13a9e0c4ed2bc4163e80648c495/aWK3iDS1Q2ar3nf-{}.ts'.format(num))
        with open('tsms4//'+num+'.ts','wb+') as f:
            f.write(conn.content)
            print(num,'下载完成')


# donload(41)

def fun1(i):
    time.sleep(0.5)
    print(i,os.getpid())
if __name__ == '__main__':
    start =time.time()
    p =Pool(4)

    p.apply_async(donload,args=(88,))


    p.close()
    p.join()
    endtime= time.time()
    print(endtime-start)