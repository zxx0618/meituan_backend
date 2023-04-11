# coding=utf-8
import numpy as np
from Incentive.common_func import *
from Incentive.common_config import *


## 返回添加中心区域的出勤补贴计算
def center_attendance(dc_cr, path, flist):  # 参数:提成数据,当前目录,目录下文件列表
    # 直接读取数据库
    # path = os.getcwd()
    # os.chdir(path)
    SQL = """
       SELECT adv.`stat_date`,
              adv.`staff_info_id` 员工工号,
              adv.`sys_store_id`,
              adv.`attendance_started_at`,
              adv.`attendance_end_at`,
              adv.`attendance_time`,
              adv.`attendance_time`*3 出勤补贴,
              hjt.`job_name`
         FROM `bi_pro`.`attendance_data_v2` adv
         LEFT JOIN `bi_pro`.`hr_job_title` hjt on adv.`job_title`= hjt.`id`
        where adv.`stat_date`>= CURRENT_DATE - INTERVAL day(CURRENT_DATE) -1 day -INTERVAL 1 month
          and adv.`stat_date`< CURRENT_DATE - INTERVAL day(CURRENT_DATE) -1 day
          and adv.`sys_store_id` IN ( 'TH01010103', 'TH01420103', 'TH01270302', 'TH01270201', 'TH01370402'
          , 'TH01300301', 'TH01090201', 'TH01290102', 'TH01460102', 'TH01360201'
          , 'TH01190101', 'TH01080109', 'TH01010202', 'TH01250101', 'TH01360102'
          , 'TH01320101', 'TH01370302', 'TH01080114', 'TH01450302', 'TH01270303'
          , 'TH01010303', 'TH01460103', 'TH01190300', 'TH01420106', 'TH01190102'
          , 'TH01360103', 'TH01010203', 'TH01300302', 'TH01420202', 'TH01420109'
          , 'TH01090202', 'TH01090101', 'TH01080138')
          and adv.`attendance_time`= 10
       """

    engine_ads = create_engine(engine_info_ads)
    # 从数据库读取结果为dataframe
    reward = pd.read_sql(SQL, engine_ads)
    engine_ads.dispose()
    writer = pd.ExcelWriter(path + '/05.中心区域出勤补贴.xlsx')
    reward.to_excel(writer, index=False)
    writer.save()
    reward_sum = pd.pivot_table(reward, index=[u'员工工号'], values=[u'出勤补贴'], aggfunc=np.sum)
    out = pd.merge(dc_cr, reward_sum, left_on='员工编号', right_on='员工工号', how='left')
    out = out.fillna(0)
    # 添加校验结果
    check = pd.DataFrame(
        {'原始字段': ['中心区域出勤补贴'], '原始数据汇总': [reward['出勤补贴'].sum()], '提成数据汇总': [out['出勤补贴'].sum()]})
    return [out, check]
