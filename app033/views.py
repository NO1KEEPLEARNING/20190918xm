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

import calendar         #获取月份有多少天

def cn_msg(requests):

    monthRange = calendar.monthrange(2019, 12)        #获取月份有多少天
    print ('monthRange',monthRange)
    print(type(monthRange[1]))
    server = '192.168.0.131'  # 数据库服务器名称或IP
    user = 'OA'  # 用户名
    password = 'Sems1991'  # 密码
    database = 'SYERP'  # 数据库名称
    port = '1433'
    conn = pymssql.connect(server, user, password, database, port)

    cursor = conn.cursor()
    MSG='2019-06-30'
    # 查询操作

    ec_name =[]



    sql = "select  CONVERT(varchar(100),a.docdate,23),a.* from VIEW_TEMP_DAY_CVT_CAP a where a.docdate='%s'  order by plantname,cc_type,in_ex desc" % (
        MSG)
    cursor.execute(sql)

    for row in cursor:
        yuefen=row[0]
        plantname =row[2]
        cc_type=row[3]

        print('row',row[0])
    return HttpResponse('1231231231231')