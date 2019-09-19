from django.shortcuts import render, HttpResponse
import pymssql
import random
import datetime


# Create your views here.
def show_msg(request):
    # color_list = ["#F5F5DC", "#00FF00", "#BA55D3", "#DC143C", "#FFD700", "#E9967A",
    #               "#90EE90", "#9932CC","#00BFFF"]
    color_list = ['write', 'write', 'write', 'write', 'write', 'write', 'write', 'write', 'write', 'write', 'write',
                  'write', 'write', 'write']
    MSG = request.GET.get('text1')
    print(MSG)
    if MSG:

        server = '192.168.0.163'  # 数据库服务器名称或IP
        user = 'OA'  # 用户名
        password = 'Sems1991'  # 密码
        database = 'SYERP'  # 数据库名称
        port = '1433'
        conn = pymssql.connect(server, user, password, database, port)

        cursor = conn.cursor()

        # 查询操作
        sql = "select  CONVERT(varchar(100),a.docdate,23),a.* from VIEW_TEMP_DAY_CVT_CAP a where a.docdate='%s'  order by plantname,cc_type,in_ex desc" % (MSG)
        cursor.execute(
            sql)
        # row = cursor.fetchone()
        # while row:
        #     print(type(row))
        #     row = cursor.fetchone()
        sc_list = []
        # 也可以使用for循环来迭代查询结果
        for row in cursor:
            # print("日期=%s, 工厂=%s ,单位=%s,组别=%s, 目标产量=%s, 当日产量=%s" % (row[0], row[1], row[2], row[3], row[4], row[5]))
            nonamec = row[0]
            docdate = row[1]  # 日期
            plantname = row[2]  # 工厂
            cc_type = row[3]  # 单位
            in_ex = row[4]  # 组别
            plan_day_qty = row[5]  # 目标产量
            day_qty = row[6]  # 当日产量
            cvt_day_qty = row[7]  # 当日换算
            work_person = row[8]  # 当日人数
            plan_day_avg_qty = row[9]  # 当日人均|目标
            plan_avg_qty = row[10]  # 当日人均|实际
            all_plan_qty = row[11]  # 累计目标
            all_qty = row[12]  # 累计产量
            all_diff = row[13]  # 差异
            all_cvt_qty = row[14]  # 累计换算
            all_avg_qty = row[15]  # 累计人均
            sc_list.append({
                "docdate": docdate,
                "plantname": plantname,
                "cc_type": cc_type,
                "in_ex": in_ex,
                "plan_day_qty": plan_day_qty,
                "day_qty": day_qty,
                "cvt_day_qty": cvt_day_qty,
                "work_person": work_person,
                "plan_day_avg_qty": plan_day_avg_qty,
                "plan_avg_qty": plan_avg_qty,
                "all_plan_qty": all_plan_qty,
                "all_qty": all_qty,
                "all_diff": all_diff,
                "all_cvt_qty": all_cvt_qty,
                "all_avg_qty": all_avg_qty

            })

        # 关闭连接
        # print('bbbbbbbbbb',sc_list)
        conn.close()
        result = []
        for el in sc_list:
            for new_el in result:
                if el['plantname'] == new_el['plantname']:
                    new_el['msg'].append({
                        "docdate": el["docdate"],
                        "cc_type": el["cc_type"],
                        "in_ex": el["in_ex"],
                        "plan_day_qty": el["plan_day_qty"],
                        "day_qty": el["day_qty"],
                        "cvt_day_qty": el["cvt_day_qty"],
                        "work_person": el["work_person"],
                        "plan_day_avg_qty": el["plan_day_avg_qty"],
                        "plan_avg_qty": el["plan_avg_qty"],
                        "all_plan_qty": el["all_plan_qty"],
                        "all_qty": el["all_qty"],
                        "all_diff": el["all_diff"],
                        "all_cvt_qty": el["all_cvt_qty"],
                        "all_avg_qty": el["all_avg_qty"]
                    })

                    break
            else:
                result.append({"plantname": el["plantname"],
                               "msg": [{
                                   "docdate": el["docdate"],
                                   "cc_type": el["cc_type"],
                                   "in_ex": el["in_ex"],
                                   "plan_day_qty": el["plan_day_qty"],
                                   "day_qty": el["day_qty"],
                                   "cvt_day_qty": el["cvt_day_qty"],
                                   "work_person": el["work_person"],
                                   "plan_day_avg_qty": el["plan_day_avg_qty"],
                                   "plan_avg_qty": el["plan_avg_qty"],
                                   "all_plan_qty": el["all_plan_qty"],
                                   "all_qty": el["all_qty"],
                                   "all_diff": el["all_diff"],
                                   "all_cvt_qty": el["all_cvt_qty"],
                                   "all_avg_qty": el["all_avg_qty"]
                               }]})

        # print("aaaa",result)
        # print("ccc",docdate)
        return render(request, '产能报表1.html', {
            "MSG": result,
            'datetime': MSG,
            "color_lsit": color_list
        })
    else:
        # print(MSG, "是空的")
        server = '192.168.0.163'  # 数据库服务器名称或IP
        user = 'OA'  # 用户名
        password = 'Sems1991'  # 密码
        database = 'SYERP'  # 数据库名称
        port = '1433'
        conn = pymssql.connect(server, user, password, database, port)

        cursor = conn.cursor()
        cursor1 = conn.cursor()

        # 查询操作
        cursor.execute(
            'select  CONVERT(varchar(100),a.docdate,23),a.* from VIEW_TEMP_DAY_CVT_CAP a  where   docdate=(select max(docdate)from VIEW_TEMP_DAY_CVT_CAP) order by plantname,cc_type,in_ex desc')
        # cursor1.execute(
        #     'select max(docdate)from VIEW_TEMP_DAY_CVT_CAP')
        # print("now_time",cursor1.fetchone())
        # row = cursor.fetchone()
        # while row:
        #     print(type(row))
        #     row = cursor.fetchone()
        sc_list = []

        # 也可以使用for循环来迭代查询结果
        for row in cursor:
            # print("日期=%s, 工厂=%s ,单位=%s,组别=%s, 目标产量=%s, 当日产量=%s" % (row[0], row[1], row[2], row[3], row[4], row[5]))
            nonamec = row[0]
            docdate = row[1]  # 日期
            plantname = row[2]  # 工厂
            cc_type = row[3]  # 单位
            in_ex = row[4]  # 组别
            plan_day_qty = row[5]  # 目标产量
            day_qty = row[6]  # 当日产量
            cvt_day_qty = row[7]  # 当日换算
            work_person = row[8]  # 当日人数
            plan_day_avg_qty = row[9]  # 当日人均|目标
            plan_avg_qty = row[10]  # 当日人均|实际
            all_plan_qty = row[11]  # 累计目标
            all_qty = row[12]  # 累计产量
            all_diff = row[13]  # 差异
            all_cvt_qty = row[14]  # 累计换算
            all_avg_qty = row[15]  # 累计人均
            sc_list.append({
                "docdate": docdate,
                "plantname": plantname,
                "cc_type": cc_type,
                "in_ex": in_ex,
                "plan_day_qty": plan_day_qty,
                "day_qty": day_qty,
                "cvt_day_qty": cvt_day_qty,
                "work_person": work_person,
                "plan_day_avg_qty": plan_day_avg_qty,
                "plan_avg_qty": plan_avg_qty,
                "all_plan_qty": all_plan_qty,
                "all_qty": all_qty,
                "all_diff": all_diff,
                "all_cvt_qty": all_cvt_qty,
                "all_avg_qty": all_avg_qty

            })

        # 关闭连接
        # print(sc_list)

        conn.close()
        result = []
        for el in sc_list:
            for new_el in result:
                if el['plantname'] == new_el['plantname']:
                    new_el['msg'].append({
                        "docdate": el["docdate"],
                        "cc_type": el["cc_type"],
                        "in_ex": el["in_ex"],
                        "plan_day_qty": el["plan_day_qty"],
                        "day_qty": el["day_qty"],
                        "cvt_day_qty": el["cvt_day_qty"],
                        "work_person": el["work_person"],
                        "plan_day_avg_qty": el["plan_day_avg_qty"],
                        "plan_avg_qty": el["plan_avg_qty"],
                        "all_plan_qty": el["all_plan_qty"],
                        "all_qty": el["all_qty"],
                        "all_diff": el["all_diff"],
                        "all_cvt_qty": el["all_cvt_qty"],
                        "all_avg_qty": el["all_avg_qty"]
                    })

                    break
            else:
                # colors=color_list.pop()
                # print(",,,,,,asd",colors)
                result.append({"plantname": el["plantname"],
                               "msg": [{
                                   "docdate": el["docdate"],
                                   "cc_type": el["cc_type"],
                                   "in_ex": el["in_ex"],
                                   "plan_day_qty": el["plan_day_qty"],
                                   "day_qty": el["day_qty"],
                                   "cvt_day_qty": el["cvt_day_qty"],
                                   "work_person": el["work_person"],
                                   "plan_day_avg_qty": el["plan_day_avg_qty"],
                                   "plan_avg_qty": el["plan_avg_qty"],
                                   "all_plan_qty": el["all_plan_qty"],
                                   "all_qty": el["all_qty"],
                                   "all_diff": el["all_diff"],
                                   "all_cvt_qty": el["all_cvt_qty"],
                                   "all_avg_qty": el["all_avg_qty"]
                               }]})
        # print(result)
        return render(request, '产能报表1.html', {
            "MSG": result,
            "now_time": docdate,
            "color_lsit": color_list

        })


# 引用模块cx_Oracle



