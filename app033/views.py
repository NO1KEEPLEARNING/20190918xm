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
    list = requests.GET.get('msg')
    print('list', list)
    if not list:
        list = '成型'
    monthRange = calendar.monthrange(2019, 12)  # 获取月份有多少天
    print('monthRange', monthRange)
    print(type(monthRange[1]))

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
    MSG = '2019-06-30'
    # 查询操作

    ec_name = []

    plan_list = []
    all_plan_list = {}
    sql0 = '''
        select  CONVERT(VARCHAR(10),docdate,23) ,plantname,cc_type,all_qty  ,all_plan_qty from VIEW_TEMP_DAY_CVT_CAP a where a.docdate='2019-06-30' and cc_type='{}' and in_ex like '%合计%' 
    ORDER BY CHARINDEX(plantname, + '双源一厂,双源二厂,自动化车间,防水车间,双源五厂,射出车间,双源八厂')
        '''.format(list)
    cursor0.execute(sql0)
    if int(len(cursor0.fetchall())):
        sql = '''
            select  CONVERT(VARCHAR(10),docdate,23) ,plantname,cc_type,all_qty  ,all_plan_qty from VIEW_TEMP_DAY_CVT_CAP a where a.docdate='2019-06-30' and cc_type='{}' and in_ex like '%合计%' 
        ORDER BY CHARINDEX(plantname, + '双源一厂,双源二厂,自动化车间,防水车间,双源五厂,射出车间,双源八厂')
            '''.format(list)
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
            all_qty = row[3]
            all_plan_qty = row[4]
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
    where a.docdate='2019-06-30' and cc_type='{}' and in_ex like '%合计%'  and plantname  in  ('双源一厂','双源二厂','自动化车间','防水车间')

        '''.format(list)
    cursor1.execute(sql1)

    zuohji = cursor1.fetchone()

    sql2 = '''
           select  sum(all_qty) ,sum(all_plan_qty) from VIEW_TEMP_DAY_CVT_CAP a
    where a.docdate='2019-06-30' and cc_type='{}' and in_ex like '%合计%'  and plantname  not  in  ('双源一厂','双源二厂','自动化车间','防水车间')

        '''.format(list)
    cursor2.execute(sql2)
    youhji = cursor2.fetchone()
    # print('zuoheji', zuohji)
    # print('youheji', youhji)

    all_plan_list['chengxing1'] = plan_list[0:4]
    all_plan_list['chengxing2'] = plan_list[4:7]

    sql3 = '''
        select  CONVERT(VARCHAR(10),docdate,23) ,plantname,cc_type, all_qty,all_plan_qty from VIEW_TEMP_DAY_CVT_CAP a
        where a.docdate='2019-06-30' and cc_type='{}'  and in_ex like '%外外包%'
    	ORDER BY CHARINDEX(plantname, + '双源一厂,双源二厂,自动化车间,防水车间,双源五厂,射出车间,双源八厂')

        '''.format(list)
    cursor3.execute(sql3)
    all_wwb_list = {}
    wwb_list = []
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

    sql4 = '''
  

select sum(all_qty) from VIEW_TEMP_DAY_CVT_CAP where cc_type ='{}'  and  docdate='2019-06-30' 
and in_ex like '%外外包%' and plantname   in  ('双源一厂','双源二厂','自动化车间','防水车间')

 GROUP BY cc_type  
    '''.format(list)
    cursor4.execute(sql4)
    wwbzuohji = cursor4.fetchone()
    print('wwbzuohji',wwbzuohji)
    sql5 = '''
       python

select sum(all_qty) from VIEW_TEMP_DAY_CVT_CAP where cc_type ='{}'  and  docdate='2019-06-30' 
and in_ex like '%外外包%'   and plantname   not  in  ('双源一厂','双源二厂','自动化车间','防水车间')

 GROUP BY cc_type  
    
    '''.format(list)
    cursor5.execute(sql5)
    wwbyouhji = cursor5.fetchone()

    sql6 = '''
           select  CONVERT(VARCHAR(10),docdate,23) ,plantname,cc_type, all_qty,all_plan_qty from VIEW_TEMP_DAY_CVT_CAP a
           where a.docdate='2019-06-30' and cc_type='{}'  and in_ex like '%内外包%'
       	ORDER BY CHARINDEX(plantname, + '双源一厂,双源二厂,自动化车间,防水车间,双源五厂,射出车间,双源八厂')

           '''.format(list)
    cursor6.execute(sql6)
    all_nwb_list = {}
    nwb_list = []
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

    sql7 = '''
            select  sum(all_qty) ,sum(all_plan_qty) from VIEW_TEMP_DAY_CVT_CAP a 
       where a.docdate='2019-06-30' and cc_type='{}' and in_ex like '%内外包%' and plantname  in  ('双源一厂','双源二厂','自动化车间','防水车间')


       '''.format(list)
    cursor7.execute(sql7)
    nwbzuohji = cursor7.fetchone()

    sql8 = '''
            select  sum(all_qty) ,sum(all_plan_qty) from VIEW_TEMP_DAY_CVT_CAP a 
       where a.docdate='2019-06-30' and cc_type='{}' and in_ex like '%内外包%' and plantname  not in  ('双源一厂','双源二厂','自动化车间','防水车间')


       '''.format(list)
    cursor8.execute(sql8)
    nwbyouhji = cursor8.fetchone()

    # print('wwbzuoheji',wwbzuohji)
    # print('wwbzyuoheji',wwbyouhji)
    # print('all_plan_list',all_plan_list)
    # print('all_wwb_list', all_wwb_list)
    return render(requests, '双源当日产量及当月累计产能状况.html', {
        'all_plan_list': all_plan_list,
        'zuoheji': zuohji,
        'youheji': youhji,
        'all_wwb_list': all_wwb_list,
        'wwbzuohji ': wwbzuohji,
        'wwbyouhji ': wwbyouhji,
        'all_nwb_list': all_nwb_list,
        'nwbzuohji ': nwbzuohji,
        'nwbyouhji ': nwbyouhji,
        'wwbzuohji': wwbzuohji

    })
