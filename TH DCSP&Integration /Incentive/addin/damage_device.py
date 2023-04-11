# coding=utf-8
import numpy as np
from Incentive.common_func import *
from Incentive.common_config import *
import os


## 说明：
## 员工可能会转岗和转网点，在此处按当天在网点出勤比例计算; 快递员清单注意剔除支援；
## 返回添加补扣工资的数据
def damage_device(dc_cr, path, flist):  # 参数:提成数据,当前目录,目录下文件列表
    # 根据文件名读取文件，获取补助金额
    os.chdir(path)
    dexcel = ""
    for ex in flist:
        exx = ex.lower().strip()
        if exx.find('维修设备') > -1:
            dexcel = ex
            rdata = pd.read_excel(path + '/' + ex)
            ramout = rdata[[u"网点ID", '维修费用']]
            ramout = pd.pivot_table(ramout, index=['网点ID'], values=['维修费用'], aggfunc=np.sum)
            # 查询获得网点应均摊人数；
            SQL = """
                     select 
                         stafflist.staff_info_id 员工编号,
                         att.sys_store_id 网点ID,
                         sum(应出勤) 应出勤
                     from 
                     (#取出有提成的快递员和主管员工名单；剔除支援的；
                     SELECT distinct ca.`staff_info_id` 
                       from `bi_pro`.`finance_courier_achievements_v3` ca
                      where ca.`stat_date`>= CURRENT_DATE - INTERVAL day(CURRENT_DATE) -1 day -INTERVAL 1 month
                        and ca.`stat_date`< CURRENT_DATE - INTERVAL day(CURRENT_DATE) -1 day
                        and ca.`store_id` !=ca.`help_store_id` # 剔除支援的；
                     UNION 

                     SELECT distinct  ca.`staff_info_id` 
                       from `bi_pro`.`finance_keeper_manager_month` ca
                      where ca.`stat_date`>= CURRENT_DATE - INTERVAL day(CURRENT_DATE) -1 day -INTERVAL 1 month
                        and ca.`stat_date`< CURRENT_DATE - INTERVAL day(CURRENT_DATE) -1 day
                      ) stafflist

                     LEFT JOIN #计算员工在各个网点的应出勤
                     (SELECT vv.`sys_store_id`,
                            vv.`staff_info_id` ,
                            COUNT(*) 应出勤
                       FROM `bi_pro`.`attendance_data_v2` vv
                       LEFT JOIN `sys_store` ss on ss.id= vv.`sys_store_id`
                       left join bi_pro.`hr_job_title` jb on jb.`id`= vv.`job_title`
                      where ss.`category` in(1,2,10,13)
                        and vv.`stat_date`>= CURRENT_DATE - INTERVAL day(CURRENT_DATE) -1 day -INTERVAL 1 month
                        and vv.`stat_date`< CURRENT_DATE - INTERVAL day(CURRENT_DATE) -1 day #and vv.`display_data`!= 'OFF'
                        and weekday(vv.`stat_date`)!= 0 #剔除周末
                      GROUP BY 1,2
                      ) att on stafflist.staff_info_id=att.staff_info_id
                     GROUP BY 1,2
                     """
            engine_ads = create_engine(engine_info_ads)
            # 从数据库读取结果为dataframe
            staffnum = pd.read_sql(SQL, engine_ads)
            engine_ads.dispose()
            radetal = pd.merge(ramout, staffnum, left_on='网点ID', right_on='网点ID', how='left')
            # 网点出勤汇部
            nwatt = pd.pivot_table(radetal, index=['网点ID'], values=['应出勤'], aggfunc=np.sum)
            nwatt = nwatt.rename(columns={u"应出勤": '网点总应出勤'})
            radetal = pd.merge(radetal, nwatt, left_on='网点ID', right_on='网点ID', how='left')
            # 每个员工应平摊维修费用
            radetal['平摊维修费用'] = round(radetal['维修费用'] * radetal['应出勤'] / radetal['网点总应出勤'], 2)
            outcome = pd.pivot_table(radetal, index=['员工编号'], values=['平摊维修费用'], aggfunc=np.sum)
            # 保存一下结果
            writer = pd.ExcelWriter(path + '/06.damage_device.xlsx')
            outcome.to_excel(writer, sheet_name='个人汇总')
            radetal.to_excel(writer, sheet_name='明细', index=False)
            writer.save()
            writer.close()
            out = pd.merge(dc_cr, outcome, left_on='员工编号', right_on='员工编号', how='left')
            out['平摊维修费用'] = out['平摊维修费用'].fillna(0)

            # 添加校验结果
            check = pd.DataFrame(
                {'原始字段': ['平摊维修费用'], '原始数据汇总': [ramout['维修费用'].sum()],
                 '提成数据汇总': [out['平摊维修费用'].sum()]})
            return [out, check]
    if dexcel == "":
        print('缺少：维修设备的数据文件！')
        return [dc_cr, pd.DataFrame([])]
