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
        self.year =''
        self.mon =''
        self.time =''
        self.gosi =''

    def twonum(self,number):
        nums ='%.2f' %number
        print(nums)
        return float(nums)
   
    def produce_sunmsg(self, request):
        '''
        各种sql 数据语句
        :param requests:
        :return:
        '''
        self.gosi =request.GET.get('carlist')
        # print('公司',self.gosi)
        self.time=request.GET.get('text1')
        # print('时间',self.time)

        if  not  (self.gosi and self.time) :
            self.gosi='XY'
            self.time ='2020-01'


            # print(self.gosi)
            # print(self.time)
        year,month = self.time.split('-')
        self.year=year
        monthRanges = calendar.monthrange(int(year), int(month))  # 获取月份有多少天
        # print('monthRange++++++',mon1, monthRange)
        manytime = monthRanges[1]
        # print('manytime',manytime)

        year_mon_day_title = year + '-' + str(month) + '-' + str(manytime)
        year_mon_1_title  = year + '-' + str(month) + '-' + str('01')
        perid_id_title  = year + '-' + str(month)


        year_last_time =datetime.date(int(year),int(month),1)-datetime.timedelta(1)   #上个月月末日期
        year_first_time=datetime.date(year_last_time.year,year_last_time.month, 1)
        # print('year_last_time',year_last_time)
        # print('year_first_time',year_first_time)


        # print('year_mon_day_title',year_mon_day_title)
        # print('year_mon_1_title,', year_mon_1_title)
        # print('perid_id_title',perid_id_title)


        cursor = self.conn.cursor()

        # 本月开单指令
        sum_order_number_sql = '''
        select count(1) 本月开单指令 from VIEW_PR_CTW where lockdate>='{}'and lockdate<='{}' and company_id='{}' and periodid='{}'AND LOTNO not like '%试作%' 
        
        '''.format(year_mon_1_title,year_mon_day_title,self.gosi,perid_id_title)
        cursor.execute(sum_order_number_sql)
        sum_order_number = cursor.fetchall()
        #print('sum_order_number--  ', sum_order_number)

        # 总共完成指令数
        mon_order_finsh_sql = '''
        select COUNT(1) 总共完成指令数 from VIEW_PR_CTW
where cpmaxdate<='{}' and cpmaxdate>='{}' AND cp_ok_flag=1 and company_id='{}'and periodid='{}'
        '''.format(year_mon_day_title,year_mon_1_title,self.gosi,perid_id_title)
        cursor.execute(mon_order_finsh_sql)
        mon_order_finsh = cursor.fetchall()
        #print('mon_order_finsh', mon_order_finsh)

        # 本月开单本月完成
        mon_order_open_finsh_sql = '''
                select COUNT(1) 本月开单本月完成 from VIEW_PR_CTW
where cpmaxdate<='{}'and  cpmaxdate>='{}'   and lockdate>='{}' and lockdate<='{}' AND cp_ok_flag=1 and company_id='{}'and periodid='{}'AND LOTNO not like '%试作%' 
                '''.format(year_mon_day_title,year_mon_day_title ,year_mon_day_title ,year_mon_day_title,self.gosi,perid_id_title )
        cursor.execute(mon_order_open_finsh_sql)
        mon_order_open_finsh = cursor.fetchall()
        #print('mon_order_open_finsh--', mon_order_open_finsh)

        # 上月开单本月完成
        last_mon_order_open_finsh_sql = '''
                        select COUNT(1) 本月开单本月完成 from VIEW_PR_CTW
        where cpmaxdate<='{}'and  cpmaxdate>='{}'   and lockdate>='{}' and lockdate<='{}' AND cp_ok_flag=1 and company_id='{}'and periodid='{}'AND LOTNO not like '%试作%' 
                        '''.format(year_mon_day_title,year_mon_day_title ,year_last_time,year_first_time,self.gosi,perid_id_title )
        cursor.execute(last_mon_order_open_finsh_sql)
        last_mon_order_open_finsh = cursor.fetchall()
        #print('last_mon_order_open_finsh_sql', last_mon_order_open_finsh)

        # 上个月之前的开单指令数本月完成
        last_after_mon_order_finsh_sql = '''
        select COUNT(distinct  lotno) 上个月之前的开单指令数本月完成 from VIEW_PR_CTW
where cpmaxdate<='{}'and  cpmaxdate>='{}'    AND cp_ok_flag=1  and lockdate<'{}' and periodid='{}'and company_id='{}'AND LOTNO not like '%试作%' 
        
        
        '''.format( year_mon_day_title, year_mon_day_title , year_last_time  ,perid_id_title,self.gosi  )
        cursor.execute(last_after_mon_order_finsh_sql)
        last_after_mon_order_finsh = cursor.fetchall()
        #print('last_after_mon_order_finsh', last_after_mon_order_finsh)

        # 当月共计完成双数

        now_mon_finsh_number_sql = '''
        select sum(cpmthQty) 当月共计完成双数 from VIEW_PR_CTW where cpmaxdate<='{}'and  cpmaxdate>='{}' and periodid='{}'and company_id='{}'AND LOTNO not like '%试作%' 
        '''.format( year_mon_day_title,year_mon_1_title,perid_id_title,self.gosi)
        cursor.execute(now_mon_finsh_number_sql)
        now_mon_finsh_number = cursor.fetchall()
        #print('now_mon_finsh_number', now_mon_finsh_number)

        # 当月开单完成双数
        now_mon_open_finsh_sql = '''
        select sum(cpmthQty) 当月开单完成双数 from VIEW_PR_CTW where cpmaxdate<='{}'and  cpmaxdate>='{}'and lockdate>='{}'and lockdate<='{}' and periodid='{}'and company_id='{}'AND LOTNO not like '%试作%' 
        
        
        '''.format(year_mon_day_title,year_mon_1_title,year_mon_1_title,year_mon_day_title,perid_id_title,self.gosi )
        cursor.execute(now_mon_open_finsh_sql)
        now_mon_open_finsh = cursor.fetchall()
        #print('now_mon_open_finsh', now_mon_open_finsh)

        # 单个指令最大开单双数

        one_order_max_number_sql = '''
        select MAX(realdigit)单个指令最大开单双数  from VIEW_PR_CTW where lockdate>='{}'and lockdate<='{}'and periodid='{}'and company_id='{}'AND LOTNO not like '%试作%' 
        
        
        '''.format(year_mon_1_title,year_mon_day_title,perid_id_title,self.gosi)

        cursor.execute(one_order_max_number_sql)
        one_order_max_number = cursor.fetchall()
        #print('one_order_max_number', one_order_max_number)

        # 单个指令最小开单双数

        one_order_min_number_sql = '''
        select Min(realdigit)单个指令最小开单双数  from VIEW_PR_CTW where lockdate>='{}'and lockdate<='{}' and periodid='{}'and company_id='{}'AND LOTNO not like '%试作%' 
        
        '''.format(year_mon_1_title,year_mon_day_title,perid_id_title,self.gosi)

        cursor.execute(one_order_min_number_sql)
        one_order_min_number = cursor.fetchall()
        #print('one_order_max_number',one_order_min_number)



        # 当月份未完成指令

        mon_order_not_finsh_sql= '''
        select  count(1) 当月份未完成指令  from VIEW_PR_CTW
where lockdate>='{}'and lockdate<='{}'  and (cp_ok_flag=0 OR 
(cpmaxdate>'{}' AND cp_ok_flag=1) ) and periodid='{}'and company_id='{}'AND LOTNO not like '%试作%' 
        
        
        
        '''.format(year_mon_1_title,year_mon_day_title,year_mon_day_title,perid_id_title,self.gosi )
        cursor.execute(mon_order_not_finsh_sql)
        mon_order_not_finsh = cursor.fetchall()
        #print('mon_order_not_finsh', mon_order_not_finsh)




        #当月份未完成指令已领料
        now_mon_order_not_finsh_hav_sql ='''
        select  count(1) 当月份未完成指令已领料  from VIEW_PR_CTW
where lockdate>='{}'and lockdate<='{}'  and (cp_ok_flag=0 OR 
(cpmaxdate>'{}' AND cp_ok_flag=1) ) and mtlckdate>='{}'and mtlckdate<='{}'   and periodid='{}'and company_id='{}'AND LOTNO not like '%试作%' 
        
        
        '''.format(year_mon_1_title,year_mon_day_title,year_mon_day_title,year_mon_1_title,year_mon_day_title,perid_id_title,self.gosi)
        cursor.execute(now_mon_order_not_finsh_hav_sql)
        now_mon_order_not_finsh_hav = cursor.fetchall()
        #print('now_mon_order_not_finsh_hav', now_mon_order_not_finsh_hav)


        #当月份未完成指令部分缴库


        now_mon_not_finsh_upon_sql='''
        
        select  count(1) 当月份未完成指令部分缴库  from VIEW_PR_CTW
where lockdate>='{}'and lockdate<='{}'  and (cp_ok_flag=0 OR 
(cpmaxdate>'{}' AND cp_ok_flag=1) ) and mtlckdate>='{}'and mtlckdate<='{}'   and cpmthQty<>0  and periodid='{}'and company_id='{}'AND LOTNO not like '%试作%' 
        
        
        '''.format(year_mon_1_title,year_mon_day_title,year_mon_day_title,year_mon_1_title,year_mon_day_title,perid_id_title,self.gosi)

        cursor.execute(now_mon_not_finsh_upon_sql)
        now_mon_not_finsh_upon = cursor.fetchall()
        #print('now_mon_not_finsh_upon', now_mon_not_finsh_upon)




        #--本月共完成指令数  首批领料与首批缴库时间差(总时长)

        order_finsh_sun_time_sql ='''
        select  sum((diff)*realdigit)/sum(realdigit) 首批与首批时间平均时长 from VIEW_PR_CTW
where cpmaxdate <='{}' and cpmaxdate>='{}' AND cp_ok_flag=1 and periodid='{}'and company_id='{}'AND LOTNO not like '%试作%' 
        
        
        '''.format(year_mon_day_title,year_mon_1_title,perid_id_title,self.gosi )

        cursor.execute(order_finsh_sun_time_sql)
        order_finsh_sun_time = cursor.fetchall()
        #print('order_finsh_sun_time',order_finsh_sun_time)

        #----本月共完成指令数  首批缴库与最后批缴库时间差

        order_finsh_1t9cha_time_sql ='''
        select  sum((diff2)*realdigit)/sum(realdigit) 首批与首批时间平均时长 from VIEW_PR_CTW 
where cpmaxdate <='{}' and cpmaxdate>='{}' AND cp_ok_flag=1 and periodid='{}'and company_id='{}'AND LOTNO not like '%试作%' 
        
        '''.format(year_mon_day_title,year_mon_1_title,perid_id_title,self.gosi )

        cursor.execute(order_finsh_1t9cha_time_sql)
        order_finsh_1t9cha_time = cursor.fetchall()
        #print('order_finsh_1t9cha_time', order_finsh_1t9cha_time)





        #--当月开单 本月完成指令数  首批领料与首批缴库时间差 开单并完成


        order_finsh_1t1cha_time_sql ='''
        select  sum((diff)*realdigit)/sum(realdigit) 首批与首批时间平均时长 from VIEW_PR_CTW
where cpmaxdate <='{}' and cpmaxdate>='{}' AND cp_ok_flag=1  and lockdate>='{}'and lockdate<='{}' and periodid='{}'and company_id='{}'AND LOTNO not like '%试作%' 
        
        
        '''.format(year_mon_day_title,year_mon_1_title,year_mon_1_title,year_mon_day_title,perid_id_title,self.gosi)

        cursor.execute(order_finsh_1t1cha_time_sql)
        order_finsh_1t1cha_time = cursor.fetchall()
        #print('order_finsh_1t1cha_time', order_finsh_1t1cha_time)
        # --当月开单 本月完成指令数 首次与最后一次缴库时间差  开单并完成
        order_finsh_1t1cha1_time_sql = '''
                    select  sum((diff2)*realdigit)/sum(realdigit) 首批与首批时间平均时长 from VIEW_PR_CTW 
where cpmaxdate <='{}' and cpmaxdate>='{}' AND cp_ok_flag=1  and lockdate>='{}'and lockdate<='{}' and periodid='{}'and company_id='{}'AND LOTNO not like '%试作%' 
               
                '''.format(year_mon_day_title,year_mon_1_title,year_mon_1_title,year_mon_day_title,perid_id_title,self.gosi)

        cursor.execute(order_finsh_1t1cha1_time_sql)
        order_finsh_1t1cha1_time = cursor.fetchall()
       # print('order_finsh_1t1cha_time', order_finsh_1t1cha1_time)

        # 本月订单缴库总(带试作)

        mon_order_mtl_sun_sql='''
       select lotno,realdigit,mtlckdate,cpmindate,diff,cpmaxdate,diff2+diff
FROM VIEW_PR_CTW 
where cpmaxdate<='{}' and cpmaxdate>='{}' AND cp_ok_flag=1 and periodid='{}'and company_id='{}'
order by diff+diff2 ASC ,realdigit DESC
        '''.format(year_mon_day_title,year_mon_1_title,perid_id_title,self.gosi)
        cursor.execute(mon_order_mtl_sun_sql)
        mon_order_mtl_sun = cursor.fetchall()
        #print('mon_order_mtl_sun', mon_order_mtl_sun)


        # 本月订单将库总(不带试作)
        mon_order_mts_sun_sql='''
        select lotno,realdigit,mtlckdate,cpmindate,diff,cpmaxdate,diff2+diff
FROM VIEW_PR_CTW 
where cpmaxdate<='{}' and cpmaxdate>='{}' AND cp_ok_flag=1 AND LOTNO not like '%试作%' and periodid='{}'and company_id='{}'
order by diff+diff2 DESC ,realdigit DESC
        
        
        '''.format(year_mon_day_title,year_mon_1_title,perid_id_title,self.gosi)

        cursor.execute(mon_order_mts_sun_sql)
        mon_order_mts_sun= cursor.fetchall()
        #print('mon_order_mts_sun', mon_order_mts_sun)





#我是分割线


        number_list =['01','02','03','04','05','06','07','08','09','10','11','12']

        mon_list =['{}','2020-02','2020-03','2020-04','2020-05','2020-06','2020-07','2020-08','2020-09','2020-10','2020-11','2020-12']
        year_mon_list =[]
        every_mon_open_finsh_order_list = []
        every_mon_finsh_order_list =[]
        order_finsh_sun_time_list =[]
        order_finsh_last_time_list =[]
        order_finsh_first_time_list =[]
        order_finsh_last2_time_list =[]
        print('year',self.year)
        # yearn =int(self.year)
        yearn =self.year
        for mon1 in number_list:
            year_mon_list.append(yearn+'-'+(mon1))
           # print(mon1)
            mon2=mon1
            mon1=int(mon1)

           # print('mon1',mon1)
           # print('yearn',yearn)
            monthRange = calendar.monthrange(int(yearn), int(mon1))  # 获取月份有多少天
           # print('monthRange++++++',mon1, monthRange)
            days=monthRange[1]


            year_mon_day =yearn+'-'+str(mon2)+'-'+str(days)
            year_mon_1=yearn+'-'+str(mon2)+'-'+str('01')
            perid_id =yearn+'-'+str(mon2)
           # print('year_mon_day',year_mon_day)
           # print('year_mon_1',year_mon_1)
           # print('perid_id',perid_id)






        #每个月  总计完成指令数

            every_mon_finsh_order_sql ='''
                   SELECT  COUNT(1)   AS cnt
    FROM VIEW_PR_CTW
    WHERE ISNULL(cp_ok_flag,0) = 1  and periodid='{}'   and  company_id='{}'  and  cpmaxdate<='{}'and  cpmaxdate>='{}'
    GROUP BY  periodid,company_id
    ORDER BY company_id,periodid 
            
            '''.format(perid_id,self.gosi,year_mon_day,year_mon_1)
            cursor.execute(every_mon_finsh_order_sql)

            every_mon_finsh_order = cursor.fetchall()
            try:
                every_mon_finsh_order=every_mon_finsh_order[0][0]
            except:
                every_mon_finsh_order=0
            print('every_mon_finsh_order',every_mon_finsh_order)



            every_mon_finsh_order_list.append( every_mon_finsh_order)


        #每个月  开单完成指令数


            every_mon_open_finsh_order_sql='''
      SELECT  COUNT(1)   AS cnt
    FROM VIEW_PR_CTW
    WHERE ISNULL(cp_ok_flag,0) = 1 and  company_id='{}' and periodid='{}' 
    and  cpmaxdate<='{}'and  cpmaxdate>='{}'and lockdate>='{}'and lockdate<='{}'
    GROUP BY  periodid,company_id
    ORDER BY company_id,periodid 
            
            
            '''.format(self.gosi,perid_id,year_mon_day,year_mon_1,year_mon_1,year_mon_day)
            cursor.execute(every_mon_open_finsh_order_sql)

            every_mon_open_finsh_order = cursor.fetchall()
            # print('every_mon_open_finsh_order',every_mon_open_finsh_order)
            try:
                every_mon_open_finsh_order = every_mon_open_finsh_order[0][0]
            except:
                every_mon_open_finsh_order = 0

            every_mon_open_finsh_order_list.append( every_mon_open_finsh_order )


          #  print('number_list', number_list)
          #  print('year_mon_list ', year_mon_list)






            # 首批领料与首批缴库之间的时间差平均时长
            order_finsh_sun_time_sql = '''

                    select  isnull(sum((diff)*realdigit)/sum(realdigit),0) 首批与首批时间平均时长 from VIEW_PR_CTW
            where cpmaxdate <='{}' and cpmaxdate>='{}' AND cp_ok_flag=1 and periodid='{}'and company_id='{}'AND LOTNO not like '%试作%' 


                    '''.format(year_mon_day,year_mon_1,perid_id,self.gosi)

            cursor.execute(order_finsh_sun_time_sql)
            order_finsh_sun_time = cursor.fetchall()
          #  print('order_finsh_sun_time ',order_finsh_sun_time )
            for imsg1 in  order_finsh_sun_time:
                order_finsh_sun_time_list.append(imsg1[0])
          #  print('order_finsh_sun_time_list', order_finsh_sun_time_list)



            #首批领料与最后一次缴库时间差平均时长

            order_finsh_last_time_sql='''
                        select  isnull(sum((diff2)*realdigit)/sum(realdigit),0) 首批与首批时间平均时长 from VIEW_PR_CTW 
where cpmaxdate <='{}' and cpmaxdate>='{}' AND cp_ok_flag=1 and periodid='{}'and company_id='{}'AND LOTNO not like '%试作%' 
            
            
            '''.format(year_mon_day,year_mon_1,perid_id,self.gosi)
            cursor.execute(order_finsh_last_time_sql)
            order_finsh_last_time = cursor.fetchall()
         #   print('order_finsh_last_time', order_finsh_last_time)
            for imsg2 in order_finsh_last_time:
                order_finsh_last_time_list.append(imsg2[0])
         #   print('order_finsh_last_time_list', order_finsh_last_time_list)

            # 当月开单完成指令首批领料与首批缴库之间的时间差
            order_finsh_first_time_sql = '''
            select  isnull(sum((diff)*realdigit)/sum(realdigit),0) 首批与首批时间平均时长 from VIEW_PR_CTW
where cpmaxdate <='{}' and cpmaxdate>='{}' AND cp_ok_flag=1  and lockdate>='{}'and lockdate<='{}' and periodid='{}'and company_id='{}'AND LOTNO not like '%试作%' 

                        '''.format(year_mon_day, year_mon_1,year_mon_day, year_mon_1,perid_id,self.gosi)
            cursor.execute(order_finsh_first_time_sql)
            order_finsh_first_time = cursor.fetchall()
        #    print('order_finsh_first_time',  order_finsh_first_time)
            for imsg3 in order_finsh_first_time:
                order_finsh_first_time_list.append(imsg3[0])
         #   print('oorder_finsh_first_time_list', order_finsh_first_time_list)

            #当月开单完成指令首批指令与最后一次缴库指令的时间差
            order_finsh_last2_time_sql = '''
                        select  isnull(sum((diff2)*realdigit)/sum(realdigit),0) 首批与首批时间平均时长 from VIEW_PR_CTW
            where cpmaxdate <='{}' and cpmaxdate>='{}' AND cp_ok_flag=1  and lockdate>='{}'and lockdate<='{}' and periodid='{}'and company_id='{}'AND LOTNO not like '%试作%' 

                                    '''.format(year_mon_day, year_mon_1, year_mon_day, year_mon_1, perid_id,self.gosi)
            cursor.execute(order_finsh_last2_time_sql)
            order_finsh_last2_time = cursor.fetchall()
        #    print('order_finsh_last2_time', order_finsh_last2_time)
            for imsg3 in order_finsh_last2_time:
                order_finsh_last2_time_list.append(imsg3[0])
        #    print('order_finsh_last2_time_list', order_finsh_last2_time_list)





        #取出每个列的所以求和
        order_sum_liat =[]
        for  number  in range(len(order_finsh_sun_time_list)):
            order_numer = (float(order_finsh_sun_time_list[number]))+ (float(order_finsh_last_time_list[number]))+(float(order_finsh_first_time_list[number]))+(float(order_finsh_last2_time_list[number]))
            order_numer ='%.2f' % order_numer
            order_sum_liat.append(float(order_numer))


        print('order_sum_liat',order_sum_liat)



        # print('mon_order_open_finsh[0][0]',mon_order_open_finsh[0][0])
        print('last_mon_order_open_finsh[0][0]',last_mon_order_open_finsh[0][0])
        print('last_after_mon_order_finsh',last_after_mon_order_finsh[0][0])
        # print('mon_order_not_finsh',mon_order_not_finsh[0][0])
        # print('now_mon_order_not_finsh_hav',now_mon_order_not_finsh_hav[0][0])
        # print('now_mon_not_finsh_upon',now_mon_not_finsh_upon[0][0])
        # print('one_order_max_number',one_order_max_number[0][0])
        # print('one_order_min_number',one_order_min_number[0][0])
        # print('now_mon_finsh_number',now_mon_finsh_number[0][0])
        # print('now_mon_open_finsh ',now_mon_open_finsh)
        print('mon_order_open_finsh_sql',mon_order_open_finsh)      # 本月开单本月完成
        # print('mon_order_finsh',mon_order_finsh)   #   # 总共完成指令数
        #
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
            'every_mon_open_finsh_order_list':every_mon_open_finsh_order_list,
            'order_sum_liat':order_sum_liat


        })
produce_show = produce_show()
