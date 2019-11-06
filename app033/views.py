from django.shortcuts import render
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
# Create your views here.

import calendar  # 获取月份有多少天


def cn_msg(requests):
    nowyear = datetime.datetime.now().year
    nowmonth = datetime.datetime.now().month
    print(nowyear, nowmonth)
    # list = requests.GET.get('msg')
    months = requests.GET.get('months')

    if not months:
        months = str(nowyear) + '-' + str(nowmonth)

    year, mon = months.split('-')
    year = int(year)
    mon = int(mon)
    print('year', year)
    print('mon', mon)

    # if not list:
    #     list = '成型'
    monthRange = calendar.monthrange(year, mon)  # 获取月份有多少天
    print('monthRange', monthRange)
    print(type(monthRange[1]))

    # print('listsssssssss', list)
    print('monthsssssssss', months)

    day = str(year) + '-' + str(mon) + '-' + str(monthRange[1])

    server = '192.168.0.131'  # 数据库服务器名称或IP
    user = 'OA'  # 用户名
    password = 'Sems1991'  # 密码
    database = 'SYERP'  # 数据库名称
    port = '1433'
    conn = pymssql.connect(server, user, password, database, port)

    cursor = conn.cursor()
    cursor0 = conn.cursor()
    cursor1 = conn.cursor()
    cursor2 = conn.cursor()
    cursor3 = conn.cursor()
    cursor4 = conn.cursor()
    cursor5 = conn.cursor()
    cursor6 = conn.cursor()
    cursor7 = conn.cursor()
    cursor8 = conn.cursor()
    cursor9 = conn.cursor()

    # 针车
    cursoq = conn.cursor()
    cursoq0 = conn.cursor()
    cursoq1 = conn.cursor()
    cursoq2 = conn.cursor()
    cursoq3 = conn.cursor()
    cursoq4 = conn.cursor()
    cursoq5 = conn.cursor()
    cursoq6 = conn.cursor()
    cursoq7 = conn.cursor()
    cursoq8 = conn.cursor()

    # 查询操作

    ec_name = []

    plan_list = []
    all_plan_list = {}
    sql0 = '''
        select  CONVERT(VARCHAR(10),docdate,23) ,plantname,cc_type,all_qty  ,all_plan_qty from VIEW_TEMP_DAY_CVT_CAP a where a.docdate='{}' and cc_type='成型' and in_ex like '%合计%' 
    ORDER BY CHARINDEX(plantname, + '双源一厂,双源二厂,自动化车间,防水车间,双源五厂,射出车间,双源八厂')
        '''.format(day)
    cursor0.execute(sql0)
    num1 = int(len(cursor0.fetchall()))
    if num1:
        sql = '''
            select  CONVERT(VARCHAR(10),docdate,23) ,plantname,cc_type,all_qty  ,all_plan_qty from VIEW_TEMP_DAY_CVT_CAP a where a.docdate='{}' and cc_type='成型' and in_ex like '%合计%' 
        ORDER BY CHARINDEX(plantname, + '双源一厂,双源二厂,自动化车间,防水车间,双源五厂,射出车间,双源八厂')
            '''.format(day)
        cursor.execute(sql)

        qchelist = []
        # print('cursor',cursor)
        # print('hahahahah',len(cursor.fetchall()))

        print('123123123123')
        for row in cursor:
            dict = {}
            yuefen = row[0]
            plantname = row[1]
            cc_type = row[2]
            all_qty = row[4]
            all_plan_qty = row[3]
            dict['plantname'] = plantname
            dict['msg'] = [yuefen, cc_type, all_qty, all_plan_qty]
            plan_list.append(dict)
        print('plan_list', plan_list)


    else:

        print('4564564646456')
        for row in range(7):
            dict = {}
            yuefen = ''
            plantname = ''
            cc_type = ''
            all_qty = ''
            all_plan_qty = ''
            dict['plantname'] = plantname
            dict['msg'] = [yuefen, cc_type, all_qty, all_plan_qty]
            plan_list.append(dict)

    sql1 = '''
           select  sum(all_qty) ,sum(all_plan_qty) from VIEW_TEMP_DAY_CVT_CAP a 
    where a.docdate='{}' and cc_type='成型' and in_ex like '%合计%'  and plantname  in  ('双源一厂','双源二厂','自动化车间','防水车间')

        '''.format(day)
    cursor1.execute(sql1)

    zuohji = cursor1.fetchone()

    sql2 = '''
           select  sum(all_qty) ,sum(all_plan_qty) from VIEW_TEMP_DAY_CVT_CAP a
    where a.docdate='{}' and cc_type='成型' and in_ex like '%合计%'  and plantname  not  in  ('双源一厂','双源二厂','自动化车间','防水车间')

        '''.format(day)
    cursor2.execute(sql2)
    youhji = cursor2.fetchone()
    # print('zuoheji', zuohji)
    # print('youheji', youhji)

    all_plan_list['chengxing1'] = plan_list[0:4]
    all_plan_list['chengxing2'] = plan_list[4:7]

    sql3 = '''
        select  CONVERT(VARCHAR(10),docdate,23) ,plantname,cc_type, all_qty,all_plan_qty from VIEW_TEMP_DAY_CVT_CAP a
        where a.docdate='{}' and cc_type='成型'  and in_ex like '%外外包%'
    	ORDER BY CHARINDEX(plantname, + '双源一厂,双源二厂,自动化车间,防水车间,双源五厂,射出车间,双源八厂')

        '''.format(day)
    cursor3.execute(sql3)
    all_wwb_list = {}
    wwb_list = []
    if num1:
        print('wwb12312312313123131213')
        for row in cursor3 or 7:
            dict = {}
            yuefen = row[0]
            plantname = row[1]
            cc_type = row[2]
            all_qty = row[3]
            all_plan_qty = row[4]
            dict['plantname'] = plantname
            dict['msg'] = [yuefen, cc_type, all_qty, all_plan_qty]
            wwb_list.append(dict)

        # print('wwb_list',wwb_list)
        all_wwb_list['chengxing1'] = wwb_list[0:4]
        all_wwb_list['chengxing2'] = wwb_list[4:7]
    else:
        print('wwb55555555555555555555555555555555')
        for row in range(7):
            dict = {}
            yuefen = ''
            plantname = ''
            cc_type = ''
            all_qty = ''
            all_plan_qty = ''
            dict['plantname'] = plantname
            dict['msg'] = [yuefen, cc_type, all_qty, all_plan_qty]
            wwb_list.append(dict)
        all_wwb_list['chengxing1'] = wwb_list[0:4]
        all_wwb_list['chengxing2'] = wwb_list[4:7]

    sql4 = '''
  

select sum(all_qty) from VIEW_TEMP_DAY_CVT_CAP where    docdate='{}'  and cc_type ='成型'  
and in_ex like '%外外包%' and plantname   in  ('双源一厂','双源二厂','自动化车间','防水车间')

 GROUP BY cc_type  
    '''.format(day)
    cursor4.execute(sql4)
    wwbzuohji = cursor4.fetchone()
    print('wwbzuohji', wwbzuohji)
    sql5 = '''

select sum(all_qty) from VIEW_TEMP_DAY_CVT_CAP where  docdate='{}'  and    cc_type ='成型' 
and in_ex like '%外外包%'   and plantname   not  in  ('双源一厂','双源二厂','自动化车间','防水车间')

 GROUP BY cc_type

    '''.format(day)
    cursor5.execute(sql5)
    wwbyouhji = cursor5.fetchone()

    sql6 = '''
           select  CONVERT(VARCHAR(10),docdate,23) ,plantname,cc_type, all_qty,all_plan_qty from VIEW_TEMP_DAY_CVT_CAP a
           where a.docdate='{}' and cc_type='成型'  and in_ex like '%内外包%'
       	ORDER BY CHARINDEX(plantname, + '双源一厂,双源二厂,自动化车间,防水车间,双源五厂,射出车间,双源八厂')

           '''.format(day)
    cursor6.execute(sql6)
    all_nwb_list = {}
    nwb_list = []
    if num1:
        print('nwb12312312312313131321')
        for row in cursor6:
            dict = {}
            yuefen = row[0]
            plantname = row[1]
            cc_type = row[2]
            all_qty = row[3]
            all_plan_qty = row[4]
            dict['plantname'] = plantname
            dict['msg'] = [yuefen, cc_type, all_qty, all_plan_qty]
            nwb_list.append(dict)

        # print('wwb_list',wwb_list)
        all_nwb_list['chengxing1'] = nwb_list[0:4]
        all_nwb_list['chengxing2'] = nwb_list[4:7]
    else:
        print('nwb555555555555555555555555555')
        for row in range(7):
            dict = {}
            yuefen = ''
            plantname = ''
            cc_type = ''
            all_qty = ''
            all_plan_qty = ''
            dict['plantname'] = plantname
            dict['msg'] = [yuefen, cc_type, all_qty, all_plan_qty]
            nwb_list.append(dict)

            # print('wwb_list',wwb_list)
        all_nwb_list['chengxing1'] = nwb_list[0:4]
        all_nwb_list['chengxing2'] = nwb_list[4:7]

    sql7 = '''
            select  sum(all_qty) ,sum(all_plan_qty) from VIEW_TEMP_DAY_CVT_CAP a 
       where a.docdate='{}' and cc_type='成型' and in_ex like '%内外包%' and plantname  in  ('双源一厂','双源二厂','自动化车间','防水车间')


       '''.format(day)
    cursor7.execute(sql7)
    nwbzuohji = cursor7.fetchone()

    sql8 = '''
            select  sum(all_qty) ,sum(all_plan_qty) from VIEW_TEMP_DAY_CVT_CAP a 
       where a.docdate='{}' and cc_type='成型' and in_ex like '%内外包%' and plantname  not in  ('双源一厂','双源二厂','自动化车间','防水车间')


       '''.format(day)
    cursor8.execute(sql8)
    nwbyouhji = cursor8.fetchone()



    # 针车查询操作
    # 查询操作

    ec_name = []

    zcplan_list = []
    zcall_plan_list = {}
    sql0 = '''
            select  CONVERT(VARCHAR(10),docdate,23) ,plantname,cc_type,all_qty  ,all_plan_qty from VIEW_TEMP_DAY_CVT_CAP a where a.docdate='{}' and cc_type='针车' and in_ex like '%合计%' 
        ORDER BY CHARINDEX(plantname, + '双源一厂,双源二厂,自动化车间,防水车间,双源五厂,射出车间,双源八厂')
            '''.format(day)
    cursoq0.execute(sql0)
    num1 = int(len(cursoq0.fetchall()))
    if num1:
        sql = '''
                select  CONVERT(VARCHAR(10),docdate,23) ,plantname,cc_type,all_qty  ,all_plan_qty from VIEW_TEMP_DAY_CVT_CAP a where a.docdate='{}' and cc_type='针车' and in_ex like '%合计%' 
            ORDER BY CHARINDEX(plantname, + '双源一厂,双源二厂,自动化车间,防水车间,双源五厂,射出车间,双源八厂')
                '''.format(day)
        cursoq.execute(sql)

        qchelist = []
        # print('cursor',cursor)
        # print('hahahahah',len(cursor.fetchall()))

        print('123123123123')
        for row in cursoq:
            dict = {}
            yuefen = row[0]
            plantname = row[1]
            cc_type = row[2]
            all_qty = row[3]
            all_plan_qty = row[4]
            dict['plantname'] = plantname
            dict['msg'] = [yuefen, cc_type, all_qty, all_plan_qty]
            zcplan_list.append(dict)
        print('zcplan_list', zcplan_list)


    else:

        print('4564564646456')
        for row in range(7):
            dict = {}
            yuefen = ''
            plantname = ''
            cc_type = ''
            all_qty = ''
            all_plan_qty = ''
            dict['plantname'] = plantname
            dict['msg'] = [yuefen, cc_type, all_qty, all_plan_qty]
            zcplan_list.append(dict)

    sql1 = '''
               select  sum(all_qty) ,sum(all_plan_qty) from VIEW_TEMP_DAY_CVT_CAP a 
        where a.docdate='{}' and cc_type='针车' and in_ex like '%合计%'  and plantname  in  ('双源一厂','双源二厂','自动化车间','防水车间')

            '''.format(day)
    cursoq1.execute(sql1)

    zczuohji1 = cursoq1.fetchone()

    sql2 = '''
               select  sum(all_qty) ,sum(all_plan_qty) from VIEW_TEMP_DAY_CVT_CAP a
        where a.docdate='{}' and cc_type='针车' and in_ex like '%合计%'  and plantname  not  in  ('双源一厂','双源二厂','自动化车间','防水车间')

            '''.format(day)
    cursoq2.execute(sql2)
    zcyouhji1 = cursoq2.fetchone()
    print('zuoheji112221', zczuohji1)
    print('youheji111222', zcyouhji1)

    zcall_plan_list['chengxing1'] = zcplan_list[0:4]
    zcall_plan_list['chengxing2'] = zcplan_list[4:7]

    sql3 = '''
            select  CONVERT(VARCHAR(10),docdate,23) ,plantname,cc_type, all_qty,all_plan_qty from VIEW_TEMP_DAY_CVT_CAP a
            where a.docdate='{}' and cc_type='针车'  and in_ex like '%外外包%'
        	ORDER BY CHARINDEX(plantname, + '双源一厂,双源二厂,自动化车间,防水车间,双源五厂,射出车间,双源八厂')

            '''.format(day)
    cursoq3.execute(sql3)
    zcall_wwb_list = {}
    zcwwb_list = []
    if num1:
        # print('wwb12312312313123131213')
        for row in cursoq3 or 7:
            dict = {}
            yuefen = row[0]
            plantname = row[1]
            cc_type = row[2]
            all_qty = row[3]
            all_plan_qty = row[4]
            dict['plantname'] = plantname
            dict['msg'] = [yuefen, cc_type, all_qty, all_plan_qty]
            zcwwb_list.append(dict)

        # print('wwb_list',wwb_list)
        zcall_wwb_list['chengxing1'] = zcwwb_list[0:4]
        zcall_wwb_list['chengxing2'] = zcwwb_list[4:7]
    else:
        # print('wwb55555555555555555555555555555555')
        for row in range(7):
            dict = {}
            yuefen = ''
            plantname = ''
            cc_type = ''
            all_qty = ''
            all_plan_qty = ''
            dict['plantname'] = plantname
            dict['msg'] = [yuefen, cc_type, all_qty, all_plan_qty]
            zcwwb_list.append(dict)
        zcall_wwb_list['chengxing1'] = zcwwb_list[0:4]
        zcall_wwb_list['chengxing2'] = zcwwb_list[4:7]

    sql4 = '''


    select sum(all_qty) from VIEW_TEMP_DAY_CVT_CAP where    docdate='{}'  and cc_type ='针车'  
    and in_ex like '%外外包%' and plantname   in  ('双源一厂','双源二厂','自动化车间','防水车间')

     GROUP BY cc_type  
        '''.format(day)
    cursoq4.execute(sql4)
    zcwwbzuohji1 = cursoq4.fetchone()
    print('zcwwbzuohji', zcwwbzuohji1)
    sql5 = '''

    select sum(all_qty) from VIEW_TEMP_DAY_CVT_CAP where  docdate='{}'  and    cc_type ='针车' 
    and in_ex like '%外外包%'   and plantname   not  in  ('双源一厂','双源二厂','自动化车间','防水车间')

     GROUP BY cc_type

        '''.format(day)
    cursoq5.execute(sql5)
    zcwwbyouhji1= cursoq5.fetchone()






    # 针车内外包
    sql6 = '''
               select  CONVERT(VARCHAR(10),docdate,23) ,plantname,cc_type, all_qty,all_plan_qty from VIEW_TEMP_DAY_CVT_CAP a
               where a.docdate='{}' and cc_type='针车'  and in_ex like '%内外包%'
           	ORDER BY CHARINDEX(plantname, + '双源一厂,双源二厂,自动化车间,防水车间,双源五厂,射出车间,双源八厂')

               '''.format(day)
    cursoq6.execute(sql6)
    zcall_nwb_list = {}
    zcnwb_list = []
    if num1:
        print('nwb12312312312313131321')
        for row in cursoq6:
            dict = {}
            yuefen = row[0]
            plantname = row[1]
            cc_type = row[2]
            all_qty = row[3]
            all_plan_qty = row[4]
            dict['plantname'] = plantname
            dict['msg'] = [yuefen, cc_type, all_qty, all_plan_qty]
            zcnwb_list.append(dict)

        # print('wwb_list',wwb_list)
        zcall_nwb_list['chengxing1'] = zcnwb_list[0:4]
        zcall_nwb_list['chengxing2'] = zcnwb_list[4:7]
    else:
        print('nwb555555555555555555555555555')
        for row in range(7):
            dict = {}
            yuefen = ''
            plantname = ''
            cc_type = ''
            all_qty = ''
            all_plan_qty = ''
            dict['plantname'] = plantname
            dict['msg'] = [yuefen, cc_type, all_qty, all_plan_qty]
            zcnwb_list.append(dict)

            # print('wwb_list',wwb_list)
        zcall_nwb_list['chengxing1'] = zcnwb_list[0:4]
        zcall_nwb_list['chengxing2'] = zcnwb_list[4:7]

    sql7 = '''
                select  sum(all_qty) ,sum(all_plan_qty) from VIEW_TEMP_DAY_CVT_CAP a 
           where a.docdate='{}' and cc_type='针车' and in_ex like '%内外包%' and plantname  in  ('双源一厂','双源二厂','自动化车间','防水车间')


           '''.format(day)
    cursoq7.execute(sql7)
    zcnwbzuohji1 = cursoq7.fetchone()

    sql8 = '''
                select  sum(all_qty) ,sum(all_plan_qty) from VIEW_TEMP_DAY_CVT_CAP a 
           where a.docdate='{}' and cc_type='针车' and in_ex like '%内外包%' and plantname  not in  ('双源一厂','双源二厂','自动化车间','防水车间')


           '''.format(day)
    cursoq8.execute(sql8)
    zcnwbyouhji1 = cursoq8.fetchone()


    zdcl = []
    sql9 = '''
    select top 100  all_qty  from VIEW_TEMP_DAY_CVT_CAP where docdate='{}' and cc_type ='组合' 
   	ORDER BY CHARINDEX(in_ex, + '大地合计,外包组合,无组合,本厂组合')
    
    '''.format(day)
    cursor9.execute(sql9)
    for cow9 in cursor9:
        zdcl.append(cow9[0])

    # print('wwbzuoheji',wwbzuohji)
    # print('wwbzyuoheji',wwbyouhji)
    # print('all_plan_list',all_plan_list)
    # print('all_wwb_list', all_wwb_list)
    return render(requests, '双源当日产量及当月累计产能状况.html', {
        'all_plan_list': all_plan_list,
        'zuoheji': zuohji,
        'youheji': youhji,
        'all_wwb_list': all_wwb_list,
        'wwbzuohji': wwbzuohji,
        'wwbyouhji': wwbyouhji,
        'all_nwb_list': all_nwb_list,
        'nwbzuohji': nwbzuohji,
        'nwbyouhji': nwbyouhji,

        'zcall_plan_list': zcall_plan_list,
        'zczuoheji1': zczuohji1,
        'zcyouheji1': zcyouhji1,
        'zcall_wwb_list': zcall_wwb_list,
        'zcwwbzuohji1': zcwwbzuohji1,
        'zcwwbyouhji1': zcwwbyouhji1,
        'zcall_nwb_list': zcall_nwb_list,
        'zcnwbzuohji1': zcnwbzuohji1,
        'zcnwbyouhji1': zcnwbyouhji1,



        # 'list':list,
        'mon': day,
        'zdcl': zdcl,
        'year':year,
        'yue':mon

    })
