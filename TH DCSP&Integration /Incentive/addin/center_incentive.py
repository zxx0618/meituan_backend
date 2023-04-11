# coding=utf-8
import numpy as np
from Incentive.common_func import *
from Incentive.common_config import *


## 返回添加中心区域的50%派件补贴
def center_incentive(dc_cr, path, flist):  # 参数:提成数据,当前目录,目录下文件列表
    # 直接读取数据库
    # path = os.getcwd()
    # os.chdir(path)
    SQL = """
       SELECT fca.`staff_info_id` 员工工号,
              fca.`store_id`,
              ss.`name`,
              sum(fca.`quantity`),
              sum(fca.`amount`) /2 '50%%派件补贴'
         FROM `bi_pro`.`finance_courier_achievements_v3` fca
         LEFT JOIN `sys_store` ss on fca.`store_id`= ss.`id`
        where fca.`stat_date` >=  CURRENT_DATE - INTERVAL day(CURRENT_DATE) -1 day -INTERVAL 1 month
          and fca.`stat_date` < CURRENT_DATE - INTERVAL day(CURRENT_DATE) -1 day
           and fca.`store_id`  IN (
         -- 工厂区域异常严重网点1.5倍补贴名单
         'TH02030505', 'TH02030401', 'TH02030303', 'TH02030107', 'TH02060106'
         , 'TH02030132', 'TH02030133', 'TH01390402', 'TH10010101', 'TH10110101'
         , 'TH24060800', 'TH24050500', 'TH20020802', 'TH20020301', 'TH20070305'
         , 'TH21060402', 'TH20070505', 'TH21060202', 'TH20070203', 'TH20070518'
         , 'TH02060133', 'TH01030308', 'TH01390202', 'TH01340103', 'TH01390602'
         , 'TH20070323', 'TH01030327', 'TH10020202'
         -- 中心网点
        ,'TH01010103', 'TH01420103', 'TH01270302', 'TH01270201', 'TH01370402'
        , 'TH01300301', 'TH01090201', 'TH01290102', 'TH01460102', 'TH01360201'
        , 'TH01190101', 'TH01080109', 'TH01010202', 'TH01250101', 'TH01360102'
        , 'TH01320101', 'TH01370302', 'TH01080114', 'TH01450302', 'TH01270303'
        , 'TH01010303', 'TH01460103', 'TH01190300', 'TH01420106', 'TH01190102'
        , 'TH01360103', 'TH01010203', 'TH01300302', 'TH01420202', 'TH01420109'
        , 'TH01090202', 'TH01090101', 'TH01080138'
         )
         and  fca.`type` =1
         AND fca.`category`=2 
        GROUP BY  fca.`staff_info_id`, fca.`store_id`
       """

    engine_ads = create_engine(engine_info_ads)
    # 从数据库读取结果为dataframe
    reward = pd.read_sql(SQL, engine_ads)
    engine_ads.dispose()
    writer = pd.ExcelWriter(path + '/05.50%派件补贴.xlsx')
    reward.to_excel(writer, index=False)
    writer.save()
    reward_sum = pd.pivot_table(reward, index=[r'员工工号'], values=[r'50%派件补贴'], aggfunc=np.sum)
    out = pd.merge(dc_cr, reward_sum, left_on='员工编号', right_on='员工工号', how='left')
    out = out.fillna(0)

    # 添加校验结果
    check = pd.DataFrame(
        {'原始字段': [r'50%派件补贴'], '原始数据汇总': [reward[r'50%派件补贴'].sum()], '提成数据汇总': [out[r'50%派件补贴'].sum()]})
    return [out, check]
