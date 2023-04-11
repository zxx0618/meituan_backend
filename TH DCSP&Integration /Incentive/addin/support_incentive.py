# coding=utf-8
import numpy as np
from Incentive.common_func import *
from Incentive.common_config import *
import pandas as pd
import os

# 除了支援补贴外，其余短时效的补贴也都放在这里了；
# ## 返回添加支援补贴的数据
##这个添加了HUB的支援
# def support_incentive(dc_cr,path,flist):#参数:提成数据,当前目录,目录下文件列表,
#        #根据文件名读取文件，获取补助金额
#        os.chdir(path)
#        dexcel = ""
#        for ex in flist:
#               exx = ex.lower().strip()
#               if exx.find('支援网点') > -1:
#                      dexcel = ex
#                      rdata = pd.read_excel(path+'/'+ex,sheet_name='支援网点')
#                      hdata = pd.read_excel(path + '/' + ex, sheet_name='支援HUB')
#                      rdata=rdata[[u"工号รหัสID",u'支援天数 กี่วัน',u'备注 หมายเหตุ']]
#                      # #添加300泰铢的补贴,添加两次
#                      ramout = rdata.append(rdata[rdata[u'备注 หมายเหตุ'].str.contains('300泰铢') == True])
#                      ramout = ramout.append(rdata[rdata[u'备注 หมายเหตุ'].str.contains('300泰铢') == True])
#                      ramout = ramout.rename(columns={u"工号รหัสID":'员工id',u'支援天数 กี่วัน':'支援补贴'})
#                      outcome = pd.pivot_table(ramout, index=['员工id'], values=['支援补贴'], aggfunc=np.sum)
#                      outcome['支援补贴']=outcome['支援补贴']*100
#
#                      hdata=hdata.rename(columns={u"工号รหัสพนักงาน":'员工id',u'补贴费用':'支援补贴'})
#                      hubout = pd.pivot_table(hdata, index=['员工id'], values=['支援补贴'], aggfunc=np.sum)
#                      outcome=outcome.append(hubout)
#                      outcome=pd.pivot_table(outcome, index=['员工id'], values=['支援补贴'], aggfunc=np.sum)
#
#                      out = pd.merge(dc_cr, outcome, left_on='员工编号', right_on='员工id', how='left')
#                      out = out.fillna(0)
#                      return out
#        if dexcel== "":
#               print('缺少：支援补贴的数据文件！')
#               return dc_cr


# 返回添加支援补贴的数据  以下为备份
## 返回添加支援补贴的数据，没添加HUB
# def support_incentive(dc_cr,path,flist):#参数:提成数据,当前目录,目录下文件列表
#        #根据文件名读取文件，获取补助金额
#        os.chdir(path)
#        dexcel = ""
#        for ex in flist:
#               exx = ex.lower().strip()
#               if exx.find('支援网点') > -1:
#                      dexcel = ex
#                      rdata= pd.read_excel(path+'/'+ex)
#                      rdata=rdata[[u"工号รหัสID",u'支援天数 กี่วัน',u'备注 หมายเหตุ']]
#                      # #添加300泰铢的补贴,添加两次
#                      ramout = rdata.append(rdata[rdata[u'备注 หมายเหตุ'].str.contains('300泰铢') == True])
#                      ramout = ramout.append(rdata[rdata[u'备注 หมายเหตุ'].str.contains('300泰铢') == True])
#                      ramout = ramout.rename(columns={u"工号รหัสID":'员工id',u'支援天数 กี่วัน':'支援补贴'})
#                      outcome = pd.pivot_table(ramout, index=['员工id'], values=['支援补贴'], aggfunc=np.sum)
#                      outcome['支援补贴']=outcome['支援补贴']*100
#                      out = pd.merge(dc_cr, outcome, left_on='员工编号', right_on='员工id', how='left')
#                      out = out.fillna(0)
#                      # 添加校验结果
#                      check = pd.DataFrame(
#                                    {'原始字段': ['支援补贴'], '原始数据汇总': [outcome['支援补贴'].sum()],
#                                     '提成数据汇总': [out['支援补贴'].sum()]})
#                      return [out, check]
#        if dexcel== "":
#               print('缺少：支援补贴的数据文件！')
#               return  [dc_cr,pd.DataFrame([])]
## 返回添加支援补贴的数据

# # 支援被贴现在放在FBI中 该版本的随着FEI添加额外补贴而废止-20220909；
# def support_courierV2(dc_cr, path, flist):  # 参数:提成数据,当前目录,目录下文件列表
#     # 根据文件名读取文件，获取补助金额
#     SQL = """
# select sup.员工编号, #添加支援奖励
#       sum(sup.help_amount)+sum(ifnull(奖励,0)) 支援补贴,
#       sum(ifnull(奖励,0)) 额外奖励
# from( # 员工使用虚拟账号时可能产生两条数据，需要去重
# SELECT distinct ifnull(vrs.staff_info_id, v3.`staff_info_id`) 员工编号,
#        v3.`stat_date`,
#        v3.`help_amount`
#   FROM `bi_pro`.`finance_courier_achievements_v3` v3
#   left join( # 查找虚拟账号
#       select ss.staff_info_id,
#            ss.sub_staff_info_id
#       from `backyard_pro`.`hr_staff_apply_support_store` ss
#      where sub_staff_info_id> 0
#   ) vrs on vrs.sub_staff_info_id= v3.staff_info_id
#  WHERE v3.`stat_date`>= CURRENT_DATE - INTERVAL DAY(CURRENT_DATE) - 1 DAY -INTERVAL 1 month
#    and v3.`stat_date`< CURRENT_DATE - INTERVAL DAY(CURRENT_DATE) - 1 DAY
#    and v3.help_amount> 0
# ) sup
#
#  left join (# 7月20额外奖励，提高门槛；
#      SELECT distinct ifnull(vrs.staff_info_id, v3.`staff_info_id`) 员工编号,
#        v3.`stat_date`,
#        v3.`amount`,
#         case
#           when (ss.`category` in (10,13)) and v3.`quantity`>=40  then 300
#           when (ss.`category` in (1,2))   and v3.`quantity`>=40  then 200
#          else 0 end as 奖励
#       FROM `bi_pro`.`finance_courier_achievements_v3` v3
#      left join `sys_store`  ss on ss.id=v3.`store_id`
#       left join( # 查找虚拟账号
#           select ss.staff_info_id,
#                ss.sub_staff_info_id
#           from `backyard_pro`.`hr_staff_apply_support_store` ss
#          where sub_staff_info_id> 0
#       ) vrs on vrs.sub_staff_info_id= v3.staff_info_id
#      where v3.`stat_date` >='2022-07-20'
#          and v3.category=2
#          and v3.`stat_date`>= CURRENT_DATE - INTERVAL DAY(CURRENT_DATE) - 1 DAY -INTERVAL 1 month
#          and v3.`stat_date`< CURRENT_DATE - INTERVAL DAY(CURRENT_DATE) - 1 DAY
#          and v3.help_amount> 0
#      ) ad  on ad.员工编号=sup.员工编号 and ad.stat_date=sup.stat_date
#
# GROUP BY 1
#        """
#     engine_ads = create_engine(engine_info_ads)
#     # 从数据库读取结果为dataframe
#     reward = pd.read_sql(SQL, engine_ads)
#     engine_ads.dispose()
#     writer = pd.ExcelWriter(path + '/07.支援补贴.xlsx')
#     reward.to_excel(writer, index=False)
#     writer.save()
#     reward = reward[['员工编号', '支援补贴']]
#     out = pd.merge(dc_cr, reward, left_on='员工编号', right_on='员工编号', how='left')
#     out['支援补贴'] = out['支援补贴'].fillna(0)
#     check = pd.DataFrame({'原始字段': ['支援补贴'], '原始数据汇总': [reward['支援补贴'].sum()],
#                           '提成数据汇总': [out['支援补贴'].sum()]})
#     return [out, check]



# 支援被贴现在放在FBI中 不和罚款相抵扣
def support_courierV2(dc_cr, path, flist):  # 参数:提成数据,当前目录,目录下文件列表
    # 支援补贴
    # 根据文件名读取文件，获取补助金额
    SQL = """ 
select sup.员工编号, #添加支援奖励
      sum(sup.help_amount)+sum(help_subsidy) 支援补贴, 
      sum(help_subsidy) 额外奖励
from( # 员工使用虚拟账号时可能产生两条数据，需要去重
SELECT distinct ifnull(vrs.staff_info_id, v3.`staff_info_id`) 员工编号,
       v3.`stat_date`,
       v3.`help_amount`,
       v3.help_subsidy
  FROM `bi_pro`.`finance_courier_achievements_v3` v3
  left join( # 查找虚拟账号
      select ss.staff_info_id,
           ss.sub_staff_info_id
      from `backyard_pro`.`hr_staff_apply_support_store` ss
     where sub_staff_info_id> 0
  ) vrs on vrs.sub_staff_info_id= v3.staff_info_id
 WHERE v3.`stat_date`>= CURRENT_DATE - INTERVAL DAY(CURRENT_DATE) - 1 DAY -INTERVAL 1 month
   and v3.`stat_date`< CURRENT_DATE - INTERVAL DAY(CURRENT_DATE) - 1 DAY
    and ( v3.help_amount> 0 or v3.help_subsidy>0)
) sup

GROUP BY 1 
       """
    engine_ads = create_engine(engine_info_ads)
    # 从数据库读取结果为dataframe
    reward = pd.read_sql(SQL, engine_ads)
    engine_ads.dispose()
    writer = pd.ExcelWriter(path + '/07.支援补贴.xlsx')
    reward.to_excel(writer, index=False)
    writer.save()
    reward = reward[['员工编号', '支援补贴']]
    out = pd.merge(dc_cr, reward, left_on='员工编号', right_on='员工编号', how='left')
    out['支援补贴'] = out['支援补贴'].fillna(0)
    check = pd.DataFrame({'原始字段': ['支援补贴'], '原始数据汇总': [reward['支援补贴'].sum()],
                          '提成数据汇总': [out['支援补贴'].sum()]})
    return [out, check]




# 人效补贴
# def OLE_incentive(dc_cr, path, flist):  # 参数:提成数据,当前目录,目录下文件列表
#     # Overall  labor effectiveness（OLE）。人效奖励
#     SQL = """
#
# select t1.'员工编号',sum(t1.'人效补贴')'人效补贴'
# from (
# select si.`staff_info_id` '员工编号',mp.name '片区',ss.`name` '网点'
# ,date(convert_tz(pi.`created_at`,'+00:00','+07:00'))'日期'
# ,date(si.`hire_date`) '入职日期'
# , jt.`job_name` ,ss.`id`  ,count( DISTINCT(pi.`pno`)) '单量'
# ,datediff(date(convert_tz(pi.`created_at`,'+00:00','+07:00')),si.`hire_date` )+1 '在职时长'
#
# ,case when datediff(date(convert_tz(pi.`created_at`,'+00:00','+07:00')),si.`hire_date` )+1 >= 30 and count( DISTINCT(pi.`pno`)) >= 100 then 100
# 	when datediff(date(convert_tz(pi.`created_at`,'+00:00','+07:00')),si.`hire_date` )+1 < 30 and count( DISTINCT(pi.`pno`)) >= 70 then 100
# else 0 end '人效补贴'
#
# from `bi_pro`.`hr_staff_info` si
# LEFT JOIN `fle_staging`.`parcel_info` pi on pi.`ticket_delivery_staff_info_id` = si.`staff_info_id`
#
# LEFT JOIN `bi_pro`.`hr_job_title` jt on jt.`id`
# LEFT JOIN `fle_staging`.`sys_store` ss on ss.`id` = si.`sys_store_id`
#
# LEFT JOIN `fle_staging`.`sys_manage_piece` mp on mp.`id` = ss.`manage_piece`
# where jt.`job_name` like 'Van Courier%'
# and si.`state` = 1
# and ss.`category` in (1)
# and si.`formal` = 1
# and si.`is_sub_staff` = 0
# and pi.`state` < 9
# and pi.`returned` = 0
# and pi.`store_weight` >= 2000
# and pi.`created_at` >= convert_tz('2022-12-01','+07:00','+00:00')
# and pi.`created_at` < convert_tz('2023-01-01','+07:00','+00:00')
# and si.`hire_date` < '2023-01-01'
# and (pi.`exhibition_length` + pi.`exhibition_width` + pi.`exhibition_height` )>= 40
# and mp.`name` like 'BKK%'
# group by 1,2,3,4,5,6,7
#     order by 10 desc
# -- order by 1,2
# )t1
#
# group by 1
# order by 2 desc
#
#        """
#     engine_ads = create_engine(engine_info_ads)
#     # 从数据库读取结果为dataframe
#     reward = pd.read_sql(SQL, engine_ads)
#     engine_ads.dispose()
#     # writer = pd.ExcelWriter(path + '/08.人效达成奖.xlsx')
#     # reward.to_excel(writer, index=False)
#     # writer.save()
#     # reward = reward[['员工编号', '支援补贴']]
#     if len(reward) == 0:
#         print('没有人效补贴！')
#         return [dc_cr, pd.DataFrame([])]
#     out = pd.merge(dc_cr, reward, left_on='员工编号', right_on='员工编号', how='left')
#     out['人效补贴'] = out['人效补贴'].fillna(0)
#     check = pd.DataFrame({'原始字段': ['人效补贴'], '原始数据汇总': [reward['人效补贴'].sum()],
#                           '提成数据汇总': [out['人效补贴'].sum()]})
#     return [out, check]

# 人效补贴,人效达成奖下线后上线了该项补贴,2022年12月1日上线
def OLE_incentive(dc_cr, path, flist):  # 参数:提成数据,当前目录,目录下文件列表
    # 根据文件名读取文件，获取补助金额
    os.chdir(path)
    dexcel = ""
    for ex in flist:
        exx = ex.lower().strip()
        if exx.find('人效补贴') > -1:
            dexcel = ex
            rdata = pd.read_excel(path + '/' + ex)
            ramout = rdata[[u"员工ID", '人效补贴']]
            # 筛选一下大于0的
            # ramout = ramout.rename(columns={u"员工ID": '员工id', '总奖励': '组长补贴'})

            outcome = pd.pivot_table(ramout, index=['员工ID'], values=['人效补贴'], aggfunc=np.sum)
            out = pd.merge(dc_cr, outcome, left_on='员工编号', right_on='员工ID', how='left')
            out = out.fillna(0)
            check = pd.DataFrame(
                {'原始字段': ['员工ID'], '原始数据汇总': [ramout[r'人效补贴'].sum()],
                 '提成数据汇总': [out[r'人效补贴'].sum()]})
            return [out, check]
    if dexcel == "":
        print('缺少：人效补贴数据文件！')
        return [dc_cr, pd.DataFrame([])]

# 20221101 上线组长补贴-对接业务方花永留
def leader_subsidy(dc_cr, path, flist):  # 参数:提成数据,当前目录,目录下文件列表
    # 根据文件名读取文件，获取补助金额
    os.chdir(path)
    dexcel = ""
    for ex in flist:
        exx = ex.lower().strip()
        if exx.find('组长补贴') > -1:
            dexcel = ex
            rdata = pd.read_excel(path + '/' + ex)
            ramout = rdata[[u"员工ID", '总奖励']]
            # 筛选一下大于0的
            ramout = ramout.rename(columns={u"员工ID": '员工id', '总奖励': '组长补贴'})

            outcome = pd.pivot_table(ramout, index=['员工id'], values=['组长补贴'], aggfunc=np.sum)
            out = pd.merge(dc_cr, outcome, left_on='员工编号', right_on='员工id', how='left')
            out = out.fillna(0)
            check = pd.DataFrame(
                {'原始字段': ['组长补贴'], '原始数据汇总': [ramout[r'组长补贴'].sum()],
                 '提成数据汇总': [out[r'组长补贴'].sum()]})
            return [out, check]
    if dexcel == "":
        print('缺少：组长补贴的数据文件！')
        return [dc_cr, pd.DataFrame([])]

# 10月提成上线 错分包裹补贴 -- 仓管
def misclassified_parcel_amount(dc_cr, path, flist):  # 参数:提成数据,当前目录,目录下文件列表
    # 根据文件名读取文件，获取补助金额
    os.chdir(path)
    dexcel = ""
    for ex in flist:
        exx = ex.lower().strip()
        if exx.find('错分包裹补贴') > -1:
            dexcel = ex
            rdata = pd.read_excel(path + '/' + ex)
            ramout = rdata[[u"员工ID", '错分包裹补贴']]
            # 筛选一下大于0的
            # ramout = ramout.rename(columns={u"组长ID": '员工id', '总奖励': '组长补贴'})

            outcome = pd.pivot_table(ramout, index=['员工ID'], values=['错分包裹补贴'], aggfunc=np.sum)
            out = pd.merge(dc_cr, outcome, left_on='员工编号', right_on='员工ID', how='left')
            out = out.fillna(0)
            check = pd.DataFrame(
                {'原始字段': ['错分包裹补贴'], '原始数据汇总': [ramout[r'错分包裹补贴'].sum()],
                 '提成数据汇总': [out[r'错分包裹补贴'].sum()]})
            return [out, check]
    if dexcel == "":
        print('缺少：错分包裹补贴的数据文件！')
        return [dc_cr, pd.DataFrame([])]


# 11月提成上线 芭提雅&普吉岛补贴，
# 两项均和不和罚款相抵扣，去芭提雅&普吉岛支援的员工也享受该项补贴
def Pattaya_Phuket_Subsidy(dc_cr, path, flist):  # 参数:提成数据,当前目录,目录下文件列表
    # 根据文件名读取文件，获取补助金额
    os.chdir(path)
    dexcel = ""
    for ex in flist:
        exx = ex.lower().strip()
        if exx.find('芭提雅&普吉岛补贴') > -1:
            dexcel = ex
            rdata = pd.read_excel(path + '/' + ex)
            ramout = rdata[[u"员工ID", '芭提雅&普吉岛补贴']]
            # 筛选一下大于0的
            # ramout = ramout.rename(columns={u"组长ID": '员工id', '总奖励': '组长补贴'})

            outcome = pd.pivot_table(ramout, index=['员工ID'], values=['芭提雅&普吉岛补贴'], aggfunc=np.sum)
            out = pd.merge(dc_cr, outcome, left_on='员工编号', right_on='员工ID', how='left')
            out = out.fillna(0)
            check = pd.DataFrame(
                {'原始字段': ['芭提雅&普吉岛补贴'], '原始数据汇总': [ramout[r'芭提雅&普吉岛补贴'].sum()],
                 '提成数据汇总': [out[r'芭提雅&普吉岛补贴'].sum()]})
            return [out, check]
    if dexcel == "":
        print('缺少：芭提雅&普吉岛补贴的数据文件！')
        return [dc_cr, pd.DataFrame([])]

# 揽收称重包裹不准确复称奖励 12月上线，仓管员
def inaccurate_weigh_reward(dc_cr, path, flist):  # 参数:提成数据,当前目录,目录下文件列表
    # 根据文件名读取文件，获取补助金额
    os.chdir(path)
    dexcel = ""
    for ex in flist:
        exx = ex.lower().strip()
        if exx.find('揽收称重不准确复称奖励') > -1:
            dexcel = ex
            rdata = pd.read_excel(path + '/' + ex)
            ramout = rdata[[u"员工ID", '揽收称重不准确复称奖励']]
            # 筛选一下大于0的
            # ramout = ramout.rename(columns={u"员工ID": '员工id', '总奖励': '组长补贴'})

            outcome = pd.pivot_table(ramout, index=['员工ID'], values=['揽收称重不准确复称奖励'], aggfunc=np.sum)
            out = pd.merge(dc_cr, outcome, left_on='员工编号', right_on='员工ID', how='left')
            out = out.fillna(0)
            check = pd.DataFrame(
                {'原始字段': ['员工ID'], '原始数据汇总': [ramout[r'揽收称重不准确复称奖励'].sum()],
                 '提成数据汇总': [out[r'揽收称重不准确复称奖励'].sum()]})
            return [out, check]
    if dexcel == "":
        print('缺少：揽收称重不准确奖励的数据文件！')
        return [dc_cr, pd.DataFrame([])]


# 曼谷和东部区域特殊补贴 -- 快递员 12月1日上线
def Bangkok_special_subsidy(dc_cr, path, flist):  # 参数:提成数据,当前目录,目录下文件列表
    # 根据文件名读取文件，获取补助金额
    os.chdir(path)
    dexcel = ""
    for ex in flist:
        exx = ex.lower().strip()
        if exx.find('曼谷和东部区域特殊补贴') > -1:
            dexcel = ex
            rdata = pd.read_excel(path + '/' + ex)
            ramout = rdata[[u"员工ID", '曼谷和东部区域特殊补贴']]
            # 筛选一下大于0的
            # ramout = ramout.rename(columns={u"员工ID": '员工id', '总奖励': '组长补贴'})

            outcome = pd.pivot_table(ramout, index=['员工ID'], values=['曼谷和东部区域特殊补贴'], aggfunc=np.sum)
            out = pd.merge(dc_cr, outcome, left_on='员工编号', right_on='员工ID', how='left')
            out = out.fillna(0)
            check = pd.DataFrame(
                {'原始字段': ['员工ID'], '原始数据汇总': [ramout[r'曼谷和东部区域特殊补贴'].sum()],
                 '提成数据汇总': [out[r'曼谷和东部区域特殊补贴'].sum()]})
            return [out, check]
    if dexcel == "":
        print('缺少：曼谷和东部区域特殊补贴的数据文件！')
        return [dc_cr, pd.DataFrame([])]



# 出勤补贴 --  12月20日上线 -- 2月28日下线
def attendance_subsidy(dc_cr, path, flist):  # 参数:提成数据,当前目录,目录下文件列表
    # 根据文件名读取文件，获取补助金额
    os.chdir(path)
    dexcel = ""
    for ex in flist:
        exx = ex.lower().strip()
        if exx.find('出勤补贴') > -1:
            dexcel = ex
            rdata = pd.read_excel(path + '/' + ex)
            ramout = rdata[[u"员工ID", '出勤补贴']]
            # 筛选一下大于0的
            # ramout = ramout.rename(columns={u"员工ID": '员工id', '总奖励': '组长补贴'})

            outcome = pd.pivot_table(ramout, index=['员工ID'], values=['出勤补贴'], aggfunc=np.sum)
            out = pd.merge(dc_cr, outcome, left_on='员工编号', right_on='员工ID', how='left')
            out = out.fillna(0)
            check = pd.DataFrame(
                {'原始字段': ['staff_info_id'], '原始数据汇总': [ramout[r'出勤补贴'].sum()],
                 '提成数据汇总': [out[r'出勤补贴'].sum()]})
            return [out, check]
    if dexcel == "":
        print('缺少：出勤补贴的数据文件！')
        return [dc_cr, pd.DataFrame([])]


# 大件操作补贴 -- 仓管员 12月1日上线
def large_operation_subsidy(dc_cr, path, flist):  # 参数:提成数据,当前目录,目录下文件列表
    # 根据文件名读取文件，获取补助金额
    os.chdir(path)
    dexcel = ""
    for ex in flist:
        exx = ex.lower().strip()
        if exx.find('大件操作补贴') > -1:
            dexcel = ex
            rdata = pd.read_excel(path + '/' + ex)
            ramout = rdata[[u"员工ID", '大件操作补贴']]
            # 筛选一下大于0的
            # ramout = ramout.rename(columns={u"员工ID": '员工id', '总奖励': '组长补贴'})

            outcome = pd.pivot_table(ramout, index=['员工ID'], values=['大件操作补贴'], aggfunc=np.sum)
            out = pd.merge(dc_cr, outcome, left_on='员工编号', right_on='员工ID', how='left')
            out = out.fillna(0)
            check = pd.DataFrame(
                {'原始字段': ['员工ID'], '原始数据汇总': [ramout[r'大件操作补贴'].sum()],
                 '提成数据汇总': [out[r'大件操作补贴'].sum()]})
            return [out, check]
    if dexcel == "":
        print('缺少：大件操作补贴的数据文件！')
        return [dc_cr, pd.DataFrame([])]




# # 7，9，10 月的上报违规奖励，快递员仓管主管均有，财务同步11月提成补发，12月要取消
# def violation_reward(dc_cr, path, flist):  # 参数:提成数据,当前目录,目录下文件列表
#     # 根据文件名读取文件，获取补助金额
#     # os.chdir(path)
#     dexcel = ""
#     for ex in flist:
#         exx = ex.lower().strip()
#         if exx.find('上报违规奖励') > -1:
#             dexcel = ex
#             rdata = pd.read_excel(ex)
#             ramout = rdata[[u"员工ID", '汇总']]
#             # 筛选一下大于0的
#             ramout = ramout.rename(columns={u'汇总': '7&9&10月上报违规奖励'})
#
#             outcome = pd.pivot_table(ramout, index=['员工ID'], values=['7&9&10月上报违规奖励'], aggfunc=np.sum)
#             out = pd.merge(dc_cr, outcome, left_on='员工编号', right_on='员工ID', how='left')
#             out = out.fillna(0)
#             check = pd.DataFrame(
#                 {'原始字段': ['7&9&10月上报违规奖励'], '原始数据汇总': [ramout[r'7&9&10月上报违规奖励'].sum()],
#                  '提成数据汇总': [out[r'7&9&10月上报违规奖励'].sum()]})
#             return [out, check]
#     if dexcel == "":
#         print('缺少：7&9&10月上报违规奖励的数据文件！')
#         return [dc_cr, pd.DataFrame([])]


