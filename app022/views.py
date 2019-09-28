from django.shortcuts import render, redirect
from django.shortcuts import render, HttpResponse
import pymssql
import random
import math
import os
from django.http import FileResponse
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
import datetime
import cx_Oracle

from dateutil import parser

import xlrd
import os


from decimal import Decimal



base_path = os.getcwd() + '\sy_msg_xsl/'

tyep = 12  # 每页显示多少个
global oldgcname
oldgcname = '双源'




nowod = ''

gcmsg = ''


# Create your views here.
def msgupload(request):
    '''
    展示上传后的界面
    :param request:
    :return:
    '''
    ##print('基础地质', base_path)

    if request.method == "GET":
        pages = request.GET.get('pages')
        ##print('pages', pages)

        if not pages:
            pages = 1
        # page = page
        servr1 = "<a href=/msgupload/?pages={0}&gcmsg=双源  class='btn btn-default btn1' >双源</a>".format(pages)
        servr2 = "<a href=/msgupload/?pages={0}&gcmsg=双联 class='btn btn-success btn1'>双联</a>".format(pages)
        servr3 = "<a href=/msgupload/?pages={0}&gcmsg=双驰 class='btn btn-info btn1'>双驰</a>".format(pages)
        servr4 = "<a href=/msgupload/?pages={0}&gcmsg=星昌 class='btn btn-warning btn1'>星昌</a>".format(pages)
        gcmsg = request.GET.get('gcmsg')
        global oldgcname
        oldgcname=oldgcname
        if not gcmsg:
            gcmsg = oldgcname
        ##print('页码', pages)
        print('工厂姓名', gcmsg)
        gcmsg = gcmsg
        # conn = cx_Oracle.connect('oa/oa@192.168.0.70:1521/ekp')  # 连接数据库
        conn = cx_Oracle.connect('oa/oa@192.168.0.70:1521/ekp')  # 连接数据库

        cursor1 = conn.cursor()

        cursor1.execute(
            "select   FD_YUEFEN,FD_GONGSI, COUNT (LIS_ID),LIS_ID   from ekp_productivity_sy WHERE FD_GONGSI='{}'  GROUP BY(LIS_ID,FD_YUEFEN,FD_GONGSI) ORDER BY FD_YUEFEN DESC".format(
                gcmsg))

        sy_msg = []
        i = 0
        #print('geshu',cursor1)
        for rows in cursor1:
            sy_msg.append(rows)
            print('rows[0]',rows[0])
            i = i + 1
        ##print('i', i)
        ##print('返回页码数', pages)
        # pages=math.ceil(pages)  # 向上取整
        pagesstart = (int(pages) - 1) * tyep  # 开始页码
        pagesend = (int(pages)) * tyep  # 结束页码
        start = pagesstart
        ##print('startpage', start)

        end = pagesend
        ##print('end', end)

        sy_msg = sy_msg[start:end]
        i = math.ceil(i / tyep) + 1
        ##print('待分页信息', sy_msg)
        page_range = range(1, i)  # 显示页码数
        next_page = int(pages) + 1
        #global oldgcname
        oldgcname = gcmsg

        return render(request, '双源数据上传.html', {
            'sy_msg': sy_msg,
            'page_range': page_range,
            'next_page': next_page,
            'servr1': servr1,
            'servr2': servr2,
            'servr3': servr3,
            'servr4': servr4,
            'oldgcname': oldgcname

        })


    elif request.method == "POST":

        avatar = request.FILES.get("customer_file", None)
        # ##print(avator.name)

    # else:
    #     redirect('msg', page=1)


def show_symsg(request, id):
    '''
    展示每页对应页数数据
    :param request:
    :param id: 页数
    :return:
    '''
    date1 = request.GET.get('text1')
    global oldgcname
    oldgcnames = oldgcname
    ##print('显示被录入公司名字', oldgcnames)

    # conn = cx_Oracle.connect('oa/oa@192.168.0.70:1521/ekp')  # 连接数据库
    conn = cx_Oracle.connect('oa/oa@192.168.0.70:1521/ekp')  # 连接数据库

    cursor1 = conn.cursor()

    cursor1.execute("""
    

select  FD_ID,FD_YUEFEN,FD_BUMEN,FD_GONGSI,FD_HUANSUANHOUCHANNENG,FD_DAKAZHEHEHOURENSHU,SHENQINGGONGSHI,SHANGBANZONGGONGSHI,
                RENJUNCHANNENG,DIANNAOCHEBIZHONG,GECHANGRENJUNCHANNENG,LIS_ID   FROM (select  FD_ID,FD_YUEFEN,FD_BUMEN,FD_GONGSI,FD_HUANSUANHOUCHANNENG,FD_DAKAZHEHEHOURENSHU,SHENQINGGONGSHI,SHANGBANZONGGONGSHI,
                RENJUNCHANNENG,DIANNAOCHEBIZHONG,GECHANGRENJUNCHANNENG,LIS_ID   from ekp_productivity_sy  WHERE LIS_ID ={} and FD_GONGSI='{}' order  by FD_ID)
    """.format(id, oldgcnames))
    sy_msg = []
    for rows in cursor1:
        rows = rows
        lisss = []
        FD_ID = rows[0]
        FD_YUEFEN = rows[1]
        FD_GONGSI = rows[2]
        FD_BUMEN = rows[3]
        FD_HUANSUANHOUCHANNENG = format((float(rows[4] or 0)*100)/100.0,'.0f')


        FD_DAKAZHEHEHOURENSHU = format((float(rows[5] or 0)*100)/100.0,'.0f')
        SHENQINGGONGSHI = format((float(rows[6] or 0)*100)/100.0,'.0f')
        SHANGBANZONGGONGSHI = format((float(rows[7] or 0)*100)/100.0,'.0f')
        RENJUNCHANNENG = format((float(rows[8] or 0)*100)/100.0,'.0f')
        try:
            DIANNAOCHEBIZHONG = "%.f%%" % (float(rows[9]) * 100)
        except:
            DIANNAOCHEBIZHONG=rows[9]


        GECHANGRENJUNCHANNENG = format((float(rows[10] or 0)*100)/100.0,'.1f')
        LIS_ID = rows[11]

        lisss.append(FD_ID)
        lisss.append(FD_YUEFEN)
        lisss.append(FD_GONGSI)
        lisss.append(FD_BUMEN)
        lisss.append(FD_HUANSUANHOUCHANNENG)
        lisss.append(FD_DAKAZHEHEHOURENSHU)
        lisss.append(SHENQINGGONGSHI)
        lisss.append(SHANGBANZONGGONGSHI)
        lisss.append(RENJUNCHANNENG)
        lisss.append(DIANNAOCHEBIZHONG)
        lisss.append(GECHANGRENJUNCHANNENG)
        lisss.append(LIS_ID)

        sy_msg.append(lisss)

    return render(request, '双源展示数据.html', {
        'sy_msg': sy_msg,
    })


def add_symsg(request):
    '''
    上传数据界面
    :param request:
    :return:
    '''
    if request.method == 'GET':
        conn = cx_Oracle.connect('oa/oa@192.168.0.70:1521/ekp')  # 连接数据库

        cursor1 = conn.cursor()
        try:
            cursor1.execute(
                "select     max(LIS_ID)   from ekp_productivity_sy   ORDER BY FD_YUEFEN DESC  ")
            global nowid
            nowid = 0

            for rows in cursor1:
                nowid = int(rows[0])
                print("GET界面nowid,TRY",nowid)
            # nowid = int(nowid) + 1
        except:
            nowid = 1
            print("GET界面nowid,EXCEPT", nowid)


        ##print('lis_id---get nowid', nowid)
        return render(request, '双源数据add界面.html', {
            'nowid': nowid,
            'gcmsg': oldgcname

        })
    else:
        timemsg1 = request.POST.get('timemsg1')
        # ##print('timemsg1', timemsg1)
        datetime_struct = parser.parse(timemsg1)
        timemsg1 = time_paid = datetime_struct.strftime('%Y-%m-%d')
        # ##print('接收到的时间', timemsg1, type(timemsg1))
        avatar = request.FILES.get("exampleInputFile")
        # ##print('add测试', avatar)
        with open(base_path + avatar.name, 'wb') as f:
            for line in avatar:
                f.write(line)

        files = xlrd.open_workbook(base_path + avatar.name)
        sheet = files.sheet_by_index(0)  # 选取sheet1表格
        row = sheet.nrows  # 列表行数
        # ##print('row', row)
        mes_lis = []
        dict1 = {}

        conn = cx_Oracle.connect('oa/oa@192.168.0.70:1521/ekp')  # 连接数据库

        cursor1 = conn.cursor()
        cursor2 = conn.cursor()

        cursor1.execute(
            "select     max(LIS_ID)   from ekp_productivity_sy   ORDER BY FD_YUEFEN DESC   ")

        timemsg11 = str(timemsg1[0:7])   # 接受到年月
        ##print('接收到的日期时间为', timemsg11)
        ##print('接收到的公司名称为', oldgcname)
        cursor2.execute(
            "SELECT distinct (FD_YUEFEN) from EKP_PRODUCTIVITY_SY WHERE FD_YUEFEN like'%{}%' and FD_GONGSI='{}'".format(
                timemsg11, oldgcname))
        try:
            the_time1 = cursor2.fetchone()[0]
        except:
            the_time1=None
        ##print('数据库中存在该月数据the1_time', the_time1)

        nowid = 0

        for rows in cursor1:
            nowid = rows[0]
            print('走的0nowid')

        if not nowid:
            nowid=0

        ##print('post,nowid', nowid)
        for i in range(2, row):
            rows = sheet.row_values(i)
            rows.append(nowid)
            rows.insert(1, timemsg1)
            mes_lis.append(rows)

        # ##print(mes_lis)   # 前段Excel 返回list 数据
        conn = cx_Oracle.connect('oa/oa@192.168.0.70:1521/ekp')  # 连接数据库

        cursor3 = conn.cursor()
        for text in mes_lis:
            ##print(text)
            FD_ID = str(text[0])
            FD_YUEFEN11 = str(text[1])
            FD_GONGSI = str(text[2])
            FD_BUMEN = str(text[3])
            FD_HUANSUANHOUCHANNENG = str(text[4])
            FD_DAKAZHEHEHOURENSHU = str(text[5])
            SHENQINGGONGSHI = str(text[6])
            SHANGBANZONGGONGSHI = str(text[7])
            RENJUNCHANNENG = str(text[8])
            DIANNAOCHEBIZHONG = str(text[9])
            GECHANGRENJUNCHANNENG = str(text[10])
            LIS_ID = str(text[11])

            # ##print('加入的内容为')
            # ##print(FD_ID, FD_YUEFEN11, FD_BUMEN, FD_GONGSI, FD_HUANSUANHOUCHANNENG, FD_DAKAZHEHEHOURENSHU,
            #       SHENQINGGONGSHI, SHANGBANZONGGONGSHI,
            #       RENJUNCHANNENG, DIANNAOCHEBIZHONG, GECHANGRENJUNCHANNENG, LIS_ID)
            # ##print('FD_YUEFEN', FD_YUEFEN11[0:7], type(FD_YUEFEN11[0:7]), '========>')
            # ##print('timemsg1', timemsg1[0:7], type(str(timemsg1[0:7])), '=====>')
            #
            # ##print("结束为==>>>>>>>>>>>>>>>")
            # ##print('cursor2.fetchone()',cursor2.fetchone())

            if the_time1:

                cursor3.execute(
                    '''UPDATE EKP_PRODUCTIVITY_SY  set FD_BUMEN='{0}',FD_HUANSUANHOUCHANNENG='{1}',FD_DAKAZHEHEHOURENSHU='{2}',SHENQINGGONGSHI='{3}',SHANGBANZONGGONGSHI='{4}',RENJUNCHANNENG='{5}',DIANNAOCHEBIZHONG='{6}',GECHANGRENJUNCHANNENG='{7}',FD_GONGSI='{8}',FD_YUEFEN='{9}' WHERE FD_ID={10}  and FD_GONGSI='{11}' and FD_YUEFEN='{12}'  '''
                        .format(
                        FD_BUMEN,
                        FD_HUANSUANHOUCHANNENG,
                        FD_DAKAZHEHEHOURENSHU,
                        SHENQINGGONGSHI,
                        SHANGBANZONGGONGSHI,
                        RENJUNCHANNENG, DIANNAOCHEBIZHONG, GECHANGRENJUNCHANNENG,
                        FD_GONGSI, FD_YUEFEN11, FD_ID, oldgcname, the_time1

                    ))
                # ##print('修改成功', "hahahahahhaah")
                conn.commit()

            else:
                LIS_ID=int(LIS_ID)+1
                cursor3.execute(
                    "INSERT INTO EKP_PRODUCTIVITY_SY VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}'   )".format(
                        FD_ID, FD_YUEFEN11, FD_BUMEN, FD_HUANSUANHOUCHANNENG, FD_DAKAZHEHEHOURENSHU, SHENQINGGONGSHI,
                        SHANGBANZONGGONGSHI,
                        RENJUNCHANNENG, DIANNAOCHEBIZHONG, GECHANGRENJUNCHANNENG, LIS_ID, FD_GONGSI

                    ))
                print(">>>>>>>>>>>>>>>>>>>>>>","新增成功",LIS_ID)
                # ##print('加入成功', 'lalalallalala')
        conn.commit()
        conn.close()  # 关闭连接
        return redirect('msg')


def cnfllmsg(request):
    if request.method == 'GET':

        ontime = datetime.datetime.now()

        month = datetime.datetime.now().replace(day=1).month
        last_month = (datetime.datetime.now().replace(day=1) - datetime.timedelta(days=1)).strftime("%Y-%m")
        ##print('nowtime',last_month)     # 上个月时间

        conn = cx_Oracle.connect('oa/oa@192.168.0.70:1521/ekp')  # 连接数据库

        cursor1 = conn.cursor()
        cursor2 = conn.cursor()
        cursor3 = conn.cursor()
        cursor4 = conn.cursor()

        cursor1.execute(
            "SELECT   *  from ekp_productivity_sy    where  FD_YUEFEN  like '{0}%' and FD_GONGSI='双驰' ".format(
                last_month))

        cursor2.execute(
            "SELECT   *  from ekp_productivity_sy    where  FD_YUEFEN  like '{0}%' and FD_GONGSI='双联' ".format(
                last_month))

        cursor3.execute(
            "SELECT   *  from ekp_productivity_sy    where  FD_YUEFEN  like '{0}%'and FD_GONGSI='双源' ".format(
                last_month))

        cursor4.execute(
            "SELECT   *  from ekp_productivity_sy    where  FD_YUEFEN  like '{0}%' and FD_GONGSI='星昌' ".format(
                last_month))

        shuangchilist = []
        shuanglianlist = []
        shuangyuanlist = []
        xiangchanglist = []

        for row1 in cursor1:
            rowmsg = []
            gongsi = row1[11]
            bumen = row1[2]
            A1 = int(float(row1[3] or 0))
            A2 = int(float(row1[4] or 0))
            A3 = int(float(row1[5] or 0))
            A4 = int(float(row1[6] or 0))
            A5 = int(float(row1[7] or 0))
            try:
                A6 = "%.f%%" % (float(row1[8]) * 100)
                print('row1[8]',row1[8])
            except:
                A6 = ''

            A7 = int(float(row1[9] or 0))

            rowmsg.append(gongsi)
            rowmsg.append(bumen)
            rowmsg.append(A1)
            rowmsg.append(A2)
            rowmsg.append(A3)
            rowmsg.append(A4)
            rowmsg.append(A5)
            rowmsg.append(A6)
            rowmsg.append(A7)

            shuangchilist.append(rowmsg)

        for row2 in cursor2:
            rowmsg = []
            gongsi = row2[11]
            bumen = row2[2]
            A1 = int(float(row2[3] or 0))
            A2 = int(float(row2[4] or 0))
            A3 = int(float(row2[5] or 0))
            A4 = int(float(row2[6] or 0))
            A5 = int(float(row2[7] or 0))
            try:
                A6 = "%.f%%" % (float(row2[8]) * 100)
                print('row2[8]',row2[8])
            except:
                A6 = ''

            A7 = int(float(row2[9] or 0))

            rowmsg.append(gongsi)
            rowmsg.append(bumen)
            rowmsg.append(A1)
            rowmsg.append(A2)
            rowmsg.append(A3)
            rowmsg.append(A4)
            rowmsg.append(A5)
            rowmsg.append(A6)
            rowmsg.append(A7)

            shuanglianlist.append(rowmsg)

        for row3 in cursor3:
            rowmsg = []
            gongsi = row3[11]
            bumen = row3[2]
            A1 = int(float(row3[3] or 0))
            A2 = int(float(row3[4] or 0))
            A3 = int(float(row3[5] or 0))
            A4 = int(float(row3[6] or 0))
            A5 = int(float(row3[7] or 0))
            try:
                A6 = "%.f%%" % (float(row3[8]) * 100)
                print('row3[8]',row3[8])
            except:
                A6 = ''

            A7 = int(float(row3[9] or 0))

            rowmsg.append(gongsi)
            rowmsg.append(bumen)
            rowmsg.append(A1)
            rowmsg.append(A2)
            rowmsg.append(A3)
            rowmsg.append(A4)
            rowmsg.append(A5)
            rowmsg.append(A6)
            rowmsg.append(A7)

            shuangyuanlist.append(rowmsg)

        for row4 in cursor4:
            rowmsg = []
            gongsi = row4[11]
            bumen = row4[2]
            A1 = int(float(row4[3] or 0))
            A2 = int(float(row4[4] or 0))
            A3 = int(float(row4[5] or 0))
            A4 = int(float(row4[6] or 0))
            A5 = int(float(row4[7] or 0))
            try:
                A6 = "%.f%%" % (float(row4[8]) * 100)
                print('row1[8]',row4[8])
            except:
                A6 = ''

            A7 = int(float(row4[9] or 0))

            rowmsg.append(gongsi)
            rowmsg.append(bumen)
            rowmsg.append(A1)
            rowmsg.append(A2)
            rowmsg.append(A3)
            rowmsg.append(A4)
            rowmsg.append(A5)
            rowmsg.append(A6)
            rowmsg.append(A7)

            xiangchanglist.append(rowmsg)
        numlis = [
            len(shuangchilist), len(shuanglianlist), len(shuangyuanlist), len(xiangchanglist)

        ]
        return render(request, '产能总报表.html', {
            "shuangchilist": shuangchilist,
            "shuanglianlist": shuanglianlist,
            "shuangyuanlist": shuangyuanlist,
            "xiangchanglist": xiangchanglist,
            'numlis': numlis,
            'times': last_month

        })

    else:
        monthtime = request.POST.get('text1')
        ##print('monthtime', monthtime)
        last_month = monthtime
        conn = cx_Oracle.connect('oa/oa@192.168.0.70:1521/ekp')  # 连接数据库

        cursor1 = conn.cursor()
        cursor2 = conn.cursor()
        cursor3 = conn.cursor()
        cursor4 = conn.cursor()

        cursor1.execute(
            "SELECT   *  from ekp_productivity_sy    where  FD_YUEFEN like '{0}%'  and FD_GONGSI='双驰' ".format(
                last_month))

        cursor2.execute(
            "SELECT   *  from ekp_productivity_sy    where  FD_YUEFEN like '{0}%'  and FD_GONGSI='双联' ".format(
                last_month))

        cursor3.execute(
            "SELECT   *  from ekp_productivity_sy    where   FD_YUEFEN like '{0}%'  and FD_GONGSI='双源' ".format(
                last_month))

        cursor4.execute(
            "SELECT   *  from ekp_productivity_sy    where   FD_YUEFEN  like '{0}%'  and FD_GONGSI='星昌' ".format(
                last_month))

        shuangchilist = []
        shuanglianlist = []
        shuangyuanlist = []
        xiangchanglist = []

        for row1 in cursor1:
            rowmsg = []
            gongsi = row1[11]
            bumen = row1[2]
            A1 = int(float(row1[3] or 0))
            A2 = int(float(row1[4] or 0))
            A3 = int(float(row1[5] or 0))
            A4 = int(float(row1[6] or 0))
            A5 = int(float(row1[7] or 0))
            try:
                A6 = "%.f%%" % (float(row1[8]) * 100)
            except:
                A6 = ''

            A7 = int(float(row1[9] or 0))

            rowmsg.append(gongsi)
            rowmsg.append(bumen)
            rowmsg.append(A1)
            rowmsg.append(A2)
            rowmsg.append(A3)
            rowmsg.append(A4)
            rowmsg.append(A5)
            rowmsg.append(A6)
            rowmsg.append(A7)

            shuangchilist.append(rowmsg)

        for row2 in cursor2:
            rowmsg = []
            gongsi = row2[11]
            bumen = row2[2]
            A1 = int(float(row2[3] or 0))
            A2 = int(float(row2[4] or 0))
            A3 = int(float(row2[5] or 0))
            A4 = int(float(row2[6] or 0))
            A5 = int(float(row2[7] or 0))
            try:
                A6 = "%.f%%" % (float(row2[8]) * 100)
            except:
                A6 = ''

            A7 = int(float(row2[9] or 0))

            rowmsg.append(gongsi)
            rowmsg.append(bumen)
            rowmsg.append(A1)
            rowmsg.append(A2)
            rowmsg.append(A3)
            rowmsg.append(A4)
            rowmsg.append(A5)
            rowmsg.append(A6)
            rowmsg.append(A7)

            shuanglianlist.append(rowmsg)

        for row3 in cursor3:
            rowmsg = []
            gongsi = row3[11]
            bumen = row3[2]
            A1 = int(float(row3[3] or 0))
            A2 = int(float(row3[4] or 0))
            A3 = int(float(row3[5] or 0))
            A4 = int(float(row3[6] or 0))
            A5 = int(float(row3[7] or 0))
            try:
                A6 = "%.f%%" % (float(row3[8]) * 100)
            except:
                A6 = ''

            A7 = int(float(row3[9] or 0))

            rowmsg.append(gongsi)
            rowmsg.append(bumen)
            rowmsg.append(A1)
            rowmsg.append(A2)
            rowmsg.append(A3)
            rowmsg.append(A4)
            rowmsg.append(A5)
            rowmsg.append(A6)
            rowmsg.append(A7)

            shuangyuanlist.append(rowmsg)

        for row4 in cursor4:
            rowmsg = []
            gongsi = row4[11]
            bumen = row4[2]
            A1 = int(float(row4[3] or 0))
            A2 = int(float(row4[4] or 0))
            A3 = int(float(row4[5] or 0))
            A4 = int(float(row4[6] or 0))
            A5 = int(float(row4[7] or 0))
            try:
                A6 = "%.f%%" % (float(row4[8]) * 100)
            except:
                A6 = ''

            A7 = int(float(row4[9] or 0))

            rowmsg.append(gongsi)
            rowmsg.append(bumen)
            rowmsg.append(A1)
            rowmsg.append(A2)
            rowmsg.append(A3)
            rowmsg.append(A4)
            rowmsg.append(A5)
            rowmsg.append(A6)
            rowmsg.append(A7)

            xiangchanglist.append(rowmsg)
        numlis = [
            len(shuangchilist), len(shuanglianlist), len(shuangyuanlist), len(xiangchanglist)

        ]
        return render(request, '产能总报表.html', {
            "shuangchilist": shuangchilist,
            "shuanglianlist": shuanglianlist,
            "shuangyuanlist": shuangyuanlist,
            "xiangchanglist": xiangchanglist,
            'numlis': numlis,
            'times': last_month

        })





def download(request):
    file = open('./sy_msg_xsl/星昌.xls', 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="demo.xlsx"'
    return response