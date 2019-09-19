# # import pymssql
# # server = '192.168.0.163'  # 数据库服务器名称或IP
# # user = 'OA'  # 用户名
# # password = 'Sems1991'  # 密码
# # database = 'SYERP'  # 数据库名称
# # conn = pymssql.connect(server, user, password, database)
# #
# # cursor = conn.cursor()
# # MSG ='2019-06-25'
# # # 查询操作
# # sql = "select  CONVERT(varchar(100),a.docdate,23),a.* from VIEW_TEMP_DAY_CVT_CAP a where a.docdate='%s'" % (MSG)
# # cursor.execute(
# #     sql)
# # # row = cursor.fetchone()
# # # while row:
# # #     print(type(row))
# # #     row = cursor.fetchone()
# # sc_list = []
# # # 也可以使用for循环来迭代查询结果
# # for row in cursor:
# #     # print("日期=%s, 工厂=%s ,单位=%s,组别=%s, 目标产量=%s, 当日产量=%s" % (row[0], row[1], row[2], row[3], row[4], row[5]))
# #     nonamec = row[0]
# #     docdate = row[1]  # 日期
# #     plantname = row[2]  # 工厂
# #     cc_type = row[3]  # 单位
# #     in_ex = row[4]  # 组别
# #     plan_day_qty = row[5]  # 目标产量
# #     day_qty = row[6]  # 当日产量
# #     cvt_day_qty = row[7]  # 当日换算
# #     work_person = row[8]  # 当日人数
# #     plan_day_avg_qty = row[9]  # 当日人均|目标
# #     plan_avg_qty = row[10]  # 当日人均|实际
# #     all_plan_qty = row[11]  # 累计目标
# #     all_qty = row[12]  # 累计产量
# #     all_diff = row[13]  # 差异
# #     all_cvt_qty = row[14]  # 累计换算
# #     all_avg_qty = row[15]  # 累计人均
# #     sc_list.append({
# #         "docdate": docdate,
# #         "plantname": plantname,
# #         "cc_type": cc_type,
# #         "in_ex": in_ex,
# #         "plan_day_qty": plan_day_qty,
# #         "day_qty": day_qty,
# #         "cvt_day_qty": cvt_day_qty,
# #         "work_person": work_person,
# #         "plan_day_avg_qty": plan_day_avg_qty,
# #         "plan_avg_qty": plan_avg_qty,
# #         "all_plan_qty": all_plan_qty,
# #         "all_qty": all_qty,
# #         "all_diff": all_diff,
# #         "all_cvt_qty": all_cvt_qty,
# #         "all_avg_qty": all_avg_qty
# #
# #     })
# #     if
# #
# # # 关闭连接
# # print(sc_list)
# # conn.close()
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# # # list =[
# # #     {"color":"red","xinghao":1 ,"chandi":"riben"},
# # #     {"color":"red","xinghao":2 ,"chandi":"dongying"},
# # #     {"color":"yellow","xinghao":1 ,"chandi":"liaoning"},
# # #     {"color":"yellow","xinghao":2 ,"chandi":"heilongjiang"},
# # #     {"color":"green","xinghao":1 ,"chandi":"qingdao"},
# # #     {"color":"green","xinghao":2 ,"chandi":"hankou"},
# # #
# # # ]
# # #
# # #
# # # [{"color":"red", "msg":[{"xinghao":1 ,"chandi":"riben"
# # #                          },
# # # "xinghao":2 ,"chandi":"dongying"}
# # # ],]
#
#
# list = [
#     {"color": "red", "xinghao": 1, "chandi": "riben"},
#     {"color": "red", "xinghao": 2, "chandi": "dongying"},
#     {"color": "yellow", "xinghao": 1, "chandi": "liaoning"},
#     {"color": "yellow", "xinghao": 2, "chandi": "heilongjiang"},
#     {"color": "green", "xinghao": 1, "chandi": "qingdao"},
#     {"color": "green", "xinghao": 2, "chandi": "hankou"},
#
# ]
# list1 =[]
# result =[]
#
# for el in list:
#     for new_el in result:
#         if el['color'] ==new_el['color']:
#             new_el['msg'].append({'xinghao':el['xinghao'],'chandi':el['chandi']})
#
#             break
#     else:
#         result.append({"color":el["color"],
#                        "msg":[{'xinghao':el['xinghao'],'chandi':el['chandi']}]})
#
#
# print(result)
# # [{"color": "red", "msg": [{"xinghao": 1, "chandi": "riben"
# #                            },
# #                           "xinghao": 2, "chandi": "dongying"}
# # ], ]

# import random
# color = ["red", "pink", "yellow", "blue", "gray", "green", "pansy"]
# print(color[random.randint(0,6)])
