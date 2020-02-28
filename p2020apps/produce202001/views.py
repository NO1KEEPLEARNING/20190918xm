# Create your views here.
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
import pymssql
import random
import math
import os
from django.http import FileResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import xlwt

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
import datetime
import cx_Oracle

from dateutil import parser
from django.views.generic.base import View
import xlrd
import os
import calendar  # 获取月份有多少天


class produce_show(View):
    def __init__(self):
        self.server = '192.168.0.131'  # 数据库服务器名称或IP

        self.user = 'OA'  # 用户名
        self.password = 'Sems1991'  # 密码
        self.database = 'SYERP'  # 数据库名称
        self.port = '1433'
        self.conn = pymssql.connect(self.server, self.user, self.password, self.database, self.port)

    def produce_sunmsg(self, request):
        '''
        各种sql 数据语句
        :param requests:
        :return:
        '''

        cursor = self.conn.cursor()

        # 本月开单指令
        sum_order_number_sql = '''
        select count(1) 本月开单指令 from VIEW_PR_CTW where lockdate>='2020-01-01'and lockdate<='2020-01-31' and company_id='XC' and periodid='2020-01'AND LOTNO not like '%试作%' 
        
        '''
        cursor.execute(sum_order_number_sql)
        sum_order_number = cursor.fetchall()
        print('sum_order_number--  ', sum_order_number)

        # 总共完成指令数
        mon_order_finsh_sql = '''
        select COUNT(1) 总共完成指令数 from VIEW_PR_CTW
where cpmaxdate<='2020-01-31' and cpmaxdate>='2020-01-01' AND cp_ok_flag=1 and company_id='XC'and periodid='2020-01'
        '''
        cursor.execute(mon_order_finsh_sql)
        mon_order_finsh = cursor.fetchall()
        print('mon_order_finsh', mon_order_finsh)

        # 本月开单本月完成
        mon_order_open_finsh_sql = '''
                select COUNT(1) 本月开单本月完成 from VIEW_PR_CTW
where cpmaxdate<='2020-01-31'and  cpmaxdate>='2020-01-01'   and lockdate>='2020-01-01' and lockdate<='2020-01-31' AND cp_ok_flag=1 and company_id='XC'and periodid='2020-01'AND LOTNO not like '%试作%' 
                '''
        cursor.execute(mon_order_open_finsh_sql)
        mon_order_open_finsh = cursor.fetchall()
        print('mon_order_open_finsh--', mon_order_open_finsh)

        # 上月开单本月完成
        last_mon_order_open_finsh_sql = '''
                        select COUNT(1) 本月开单本月完成 from VIEW_PR_CTW
        where cpmaxdate<='2020-01-31'and  cpmaxdate>='2020-01-01'   and lockdate>='2020-01-01' and lockdate<='2020-01-31' AND cp_ok_flag=1 and company_id='XC'and periodid='2020-01'AND LOTNO not like '%试作%' 
                        '''
        cursor.execute(last_mon_order_open_finsh_sql)
        last_mon_order_open_finsh = cursor.fetchall()
        print('last_mon_order_open_finsh_sql', last_mon_order_open_finsh)

        # 上个月之前的开单指令数本月完成
        last_after_mon_order_finsh_sql = '''
        select COUNT(distinct  lotno) 上个月之前的开单指令数本月完成 from VIEW_PR_CTW
where cpmaxdate<='2020-01-31'and  cpmaxdate>='2020-01-01'    AND cp_ok_flag=1  and lockdate<'2019-12-01' and periodid='2020-01'and company_id='XC'AND LOTNO not like '%试作%' 
        
        
        '''
        cursor.execute(last_after_mon_order_finsh_sql)
        last_after_mon_order_finsh = cursor.fetchall()
        print('last_after_mon_order_finsh', last_after_mon_order_finsh)

        # 当月共计完成双数

        now_mon_finsh_number_sql = '''
        select sum(cpmthQty) 当月共计完成双数 from VIEW_PR_CTW where cpmaxdate<='2020-01-31'and  cpmaxdate>='2020-01-01' and periodid='2020-01'and company_id='XC'AND LOTNO not like '%试作%' 
        '''
        cursor.execute(now_mon_finsh_number_sql)
        now_mon_finsh_number = cursor.fetchall()
        print('now_mon_finsh_number', now_mon_finsh_number)

        # 当月开单完成双数
        now_mon_open_finsh_sql = '''
        select sum(cpmthQty) 当月开单完成双数 from VIEW_PR_CTW where cpmaxdate<='2020-01-31'and  cpmaxdate>='2020-01-01'and lockdate>='2020-01-01'and lockdate<='2020-01-31' and periodid='2020-01'and company_id='XC'AND LOTNO not like '%试作%' 
        
        
        '''
        cursor.execute(now_mon_open_finsh_sql)
        now_mon_open_finsh = cursor.fetchall()
        print('now_mon_open_finsh', now_mon_open_finsh)

        # 单个指令最大开单双数

        one_order_max_number_sql = '''
        select MAX(realdigit)单个指令最大开单双数  from VIEW_PR_CTW where lockdate>='2020-01-01'and lockdate<='2020-01-31'and periodid='2020-01'and company_id='XC'AND LOTNO not like '%试作%' 
        
        
        '''

        cursor.execute(one_order_max_number_sql)
        one_order_max_number = cursor.fetchall()
        print('one_order_max_number', one_order_max_number)

        # 单个指令最小开单双数

        one_order_min_number_sql = '''
        select Min(realdigit)单个指令最小开单双数  from VIEW_PR_CTW where lockdate>='2020-01-01'and lockdate<='2020-01-31' and periodid='2020-01'and company_id='XC'AND LOTNO not like '%试作%' 
        
        '''

        cursor.execute(one_order_min_number_sql)
        one_order_min_number = cursor.fetchall()
        print('one_order_max_number',one_order_min_number)



        # 当月份未完成指令

        mon_order_not_finsh_sql= '''
        select  count(1) 当月份未完成指令  from VIEW_PR_CTW
where lockdate>='2020-01-01'and lockdate<='2020-01-31'  and (cp_ok_flag=0 OR 
(cpmaxdate>'2020-01-31' AND cp_ok_flag=1) ) and periodid='2020-01'and company_id='XC'AND LOTNO not like '%试作%' 
        
        
        
        '''
        cursor.execute(mon_order_not_finsh_sql)
        mon_order_not_finsh = cursor.fetchall()
        print('mon_order_not_finsh', mon_order_not_finsh)




        #当月份未完成指令已领料
        now_mon_order_not_finsh_hav_sql ='''
        select  count(1) 当月份未完成指令已领料  from VIEW_PR_CTW
where lockdate>='2020-01-01'and lockdate<='2020-01-31'  and (cp_ok_flag=0 OR 
(cpmaxdate>'2020-01-31' AND cp_ok_flag=1) ) and mtlckdate>='2020-01-01'and mtlckdate<='2020-01-31'   and periodid='2020-01'and company_id='XC'AND LOTNO not like '%试作%' 
        
        
        '''
        cursor.execute(now_mon_order_not_finsh_hav_sql)
        now_mon_order_not_finsh_hav = cursor.fetchall()
        print('now_mon_order_not_finsh_hav', now_mon_order_not_finsh_hav)


        #当月份未完成指令部分缴库


        now_mon_not_finsh_upon_sql='''
        
        select  count(1) 当月份未完成指令部分缴库  from VIEW_PR_CTW
where lockdate>='2020-01-01'and lockdate<='2020-01-31'  and (cp_ok_flag=0 OR 
(cpmaxdate>'2020-01-31' AND cp_ok_flag=1) ) and mtlckdate>='2020-01-01'and mtlckdate<='2020-01-31'   and cpmthQty<>0  and periodid='2020-01'and company_id='XC'AND LOTNO not like '%试作%' 
        
        
        '''

        cursor.execute(now_mon_not_finsh_upon_sql)
        now_mon_not_finsh_upon = cursor.fetchall()
        print('now_mon_not_finsh_upon', now_mon_not_finsh_upon)




        #--本月共完成指令数  首批领料与首批缴库时间差(总时长)

        order_finsh_sun_time_sql ='''
        select  sum((diff)*realdigit)/sum(realdigit) 首批与首批时间平均时长 from VIEW_PR_CTW
where cpmaxdate <='2020-01-31' and cpmaxdate>='2020-01-01' AND cp_ok_flag=1 and periodid='2020-01'and company_id='XC'AND LOTNO not like '%试作%' 
        
        
        '''

        cursor.execute(order_finsh_sun_time_sql)
        order_finsh_sun_time = cursor.fetchall()
        print('order_finsh_sun_time',order_finsh_sun_time)

        #----本月共完成指令数  首批缴库与最后批缴库时间差

        order_finsh_1t9cha_time_sql ='''
        select  sum((diff2)*realdigit)/sum(realdigit) 首批与首批时间平均时长 from VIEW_PR_CTW 
where cpmaxdate <='2020-01-31' and cpmaxdate>='2020-01-01' AND cp_ok_flag=1 and periodid='2020-01'and company_id='XC'AND LOTNO not like '%试作%' 
        
        '''

        cursor.execute(order_finsh_1t9cha_time_sql)
        order_finsh_1t9cha_time = cursor.fetchall()
        print('order_finsh_1t9cha_time', order_finsh_1t9cha_time)





        #--当月开单 本月完成指令数  首批领料与首批缴库时间差 开单并完成


        order_finsh_1t1cha_time_sql ='''
        select  sum((diff)*realdigit)/sum(realdigit) 首批与首批时间平均时长 from VIEW_PR_CTW
where cpmaxdate <='2020-01-31' and cpmaxdate>='2020-01-01' AND cp_ok_flag=1  and lockdate>='2020-01-01'and lockdate<='2020-01-31' and periodid='2020-01'and company_id='XC'AND LOTNO not like '%试作%' 
        
        
        '''

        cursor.execute(order_finsh_1t1cha_time_sql)
        order_finsh_1t1cha_time = cursor.fetchall()
        print('order_finsh_1t1cha_time', order_finsh_1t1cha_time)
        # --当月开单 本月完成指令数 首次与最后一次缴库时间差  开单并完成
        order_finsh_1t1cha1_time_sql = '''
                    select  sum((diff2)*realdigit)/sum(realdigit) 首批与首批时间平均时长 from VIEW_PR_CTW 
where cpmaxdate <='2020-01-31' and cpmaxdate>='2020-01-01' AND cp_ok_flag=1  and lockdate>='2020-01-01'and lockdate<='2020-01-31' and periodid='2020-01'and company_id='XC'AND LOTNO not like '%试作%' 
               
                '''

        cursor.execute(order_finsh_1t1cha1_time_sql)
        order_finsh_1t1cha1_time = cursor.fetchall()
        print('order_finsh_1t1cha_time', order_finsh_1t1cha1_time)

        # 本月订单缴库总(带试作)

        mon_order_mtl_sun_sql='''
       select lotno,realdigit,mtlckdate,cpmindate,diff,cpmaxdate,diff2+diff
FROM VIEW_PR_CTW 
where cpmaxdate<='2020-01-31' and cpmaxdate>='2020-01-01' AND cp_ok_flag=1 and periodid='2020-01'and company_id='XC'
order by diff+diff2 ASC ,realdigit DESC
        '''
        cursor.execute(mon_order_mtl_sun_sql)
        mon_order_mtl_sun = cursor.fetchall()
        #print('mon_order_mtl_sun', mon_order_mtl_sun)


        # 本月订单将库总(不带试作)
        mon_order_mts_sun_sql='''
        select lotno,realdigit,mtlckdate,cpmindate,diff,cpmaxdate,diff2+diff
FROM VIEW_PR_CTW 
where cpmaxdate<='2020-01-31' and cpmaxdate>='2020-01-01' AND cp_ok_flag=1 AND LOTNO not like '%试作%' and periodid='2020-01'and company_id='XC'
order by diff+diff2 DESC ,realdigit DESC
        
        
        '''

        cursor.execute(mon_order_mts_sun_sql)
        mon_order_mts_sun= cursor.fetchall()
        #print('mon_order_mts_sun', mon_order_mts_sun)





#我是分割线


        number_list =['01','02','03','04','05','06','07','08','09','10','11','12']

        mon_list =['2020-01','2020-02','2020-03','2020-04','2020-05','2020-06','2020-07','2020-08','2020-09','2020-10','2020-11','2020-12']
        year_mon_list =[]
        every_mon_open_finsh_order_list = []
        every_mon_finsh_order_list =[]
        order_finsh_sun_time_list =[]

        yearn ='2020'
        for mon1 in number_list:
            year_mon_list.append(yearn+'-'+(mon1))
            print(mon1)
            mon2=mon1
            mon1=int(mon1)

            print('mon1',mon1)
            print('yearn',yearn)
            monthRange = calendar.monthrange(int(yearn), int(mon1))  # 获取月份有多少天
            print('monthRange++++++',mon1, monthRange)
            days=monthRange[1]


            year_mon_day =yearn+'-'+str(mon2)+'-'+str(days)
            year_mon_1=yearn+'-'+str(mon2)+'-'+str('01')
            perid_id =yearn+'-'+str(mon2)
            print('year_mon_day',year_mon_day)
            print('year_mon_1',year_mon_1)
            print('perid_id',perid_id)






        #每个月  总计完成指令数

            every_mon_finsh_order_sql ='''
                   SELECT  COUNT(1)   AS cnt
    FROM VIEW_PR_CTW
    WHERE ISNULL(cp_ok_flag,0) = 1  and periodid='{}'   and  company_id='xc'  and  cpmaxdate<='{}'and  cpmaxdate>='{}'
    GROUP BY  periodid,company_id
    ORDER BY company_id,periodid 
            
            '''.format(perid_id,year_mon_day,year_mon_1)
            cursor.execute(every_mon_finsh_order_sql)

            every_mon_finsh_order = cursor.fetchall()

            for imsg in every_mon_finsh_order:
                every_mon_finsh_order_list.append(imsg[0])

        #每个月  开单完成指令数


            every_mon_open_finsh_order_sql='''
      SELECT  COUNT(1)   AS cnt
    FROM VIEW_PR_CTW
    WHERE ISNULL(cp_ok_flag,0) = 1 and  company_id='xc' and periodid='{}' 
    and  cpmaxdate<='{}'and  cpmaxdate>='{}'and lockdate>='{}'and lockdate<='{}'
    GROUP BY  periodid,company_id
    ORDER BY company_id,periodid 
            
            
            '''.format(perid_id,year_mon_day,year_mon_1,year_mon_1,year_mon_day)
            cursor.execute(every_mon_open_finsh_order_sql)

            every_mon_open_finsh_order = cursor.fetchall()

            for imsg1 in every_mon_open_finsh_order:
                every_mon_open_finsh_order_list.append(imsg1[0])
            print('number_list', number_list)
            print('year_mon_list ', year_mon_list)





            order_finsh_sun_time_sql = '''

                    select  sum((diff)*realdigit)/sum(realdigit) 首批与首批时间平均时长 from VIEW_PR_CTW
            where cpmaxdate <='2020-01-31' and cpmaxdate>='2020-01-01' AND cp_ok_flag=1 and periodid='2020-01'and company_id='XC'AND LOTNO not like '%试作%' 


                    '''

            cursor.execute(order_finsh_sun_time_sql)
            order_finsh_sun_time = cursor.fetchall()
            print('order_finsh_sun_time ',order_finsh_sun_time )
            for imsg1 in  order_finsh_sun_time:
                order_finsh_sun_time_list.append(imsg1[0])
            print('order_finsh_sun_time_list', order_finsh_sun_time_list)





        print('mon_order_open_finsh[0][0]',mon_order_open_finsh[0][0])
        print('last_mon_order_open_finsh[0][0]',last_mon_order_open_finsh[0][0])
        print('last_after_mon_order_finsh',last_after_mon_order_finsh[0][0])
        print('mon_order_not_finsh',mon_order_not_finsh[0][0])
        print('now_mon_order_not_finsh_hav',now_mon_order_not_finsh_hav[0][0])
        print('now_mon_not_finsh_upon',now_mon_not_finsh_upon[0][0])
        print('one_order_max_number',one_order_max_number[0][0])
        print('one_order_min_number',one_order_min_number[0][0])
        print('now_mon_finsh_number',now_mon_finsh_number[0][0])
        print('now_mon_open_finsh ',now_mon_open_finsh)
        print('mon_order_open_finsh_sql',mon_order_open_finsh)      # 本月开单本月完成
        print('mon_order_finsh',mon_order_finsh)   #   # 总共完成指令数

        print('every_mon_finsh_order',every_mon_finsh_order_list)   #每年12个月每个月 完成指令数
        print('every_mon_open_finsh_order_list',every_mon_open_finsh_order_list)

        # return JsonResponse({'result': 200, 'msg': '连接成功','now_mon_not_finsh_upon':mon_order_mts_sun
        #                      })

        return render(request,'demi1.html',{
            'mon_order_open_finsh':mon_order_open_finsh[0][0],
            'last_mon_order_open_finsh':last_mon_order_open_finsh[0][0],
            'last_after_mon_order_finsh':last_after_mon_order_finsh[0][0],
            'mon_order_not_finsh':mon_order_not_finsh[0][0],
            'now_mon_order_not_finsh_hav':now_mon_order_not_finsh_hav[0][0],
            'now_mon_not_finsh_upon':now_mon_not_finsh_upon[0][0],
            'one_order_max_number':one_order_max_number[0][0],
            'one_order_min_number':one_order_min_number[0][0],
            'now_mon_finsh_number':now_mon_finsh_number[0][0],
            'now_mon_open_finsh':now_mon_open_finsh[0][0],
            'mon_order_finsh':mon_order_finsh[0][0],
            'every_mon_finsh_order_list':every_mon_finsh_order_list,
            'every_mon_open_finsh_order_list':every_mon_open_finsh_order_list


        })
produce_show = produce_show()