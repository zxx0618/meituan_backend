# coding=utf-8
import numpy as np
from Incentive.common_func import *
from Incentive.common_config import *


## wangnai补贴
def wongnai_reward(dc_cr, path, flist):  # 参数:提成数据,当前目录,目录下文件列表
    # 直接读取数据库
    # path = os.getcwd()
    # os.chdir(path)
    SQL = """
select pi.`ticket_pickup_staff_info_id` 员工编号,
       COUNT(*)*20 wongnai补贴
  from `fle_staging`.`parcel_info` pi
 where pi.`client_id` in ('AA0678', 'AA0680', 'AA0682', 'AA0684')
   and pi.`created_at`>= convert_tz(CURRENT_DATE - INTERVAL day(CURRENT_DATE) -1 day -INTERVAL 1 month, '+07:00', '+00:00')
   and pi.`created_at`< convert_tz(CURRENT_DATE - INTERVAL day(CURRENT_DATE) -1 day, '+07:00', '+00:00')
   and pi.`returned`= 0
   and pi.`state`< 9
   and pi.handover_thailandpost_enabled !=1
 GROUP BY 1
       """

    engine_ads = create_engine(engine_info_ads)
    # 从数据库读取结果为dataframe
    reward = pd.read_sql(SQL, engine_ads)
    engine_ads.dispose()
    # writer = pd.ExcelWriter(path + '/08.wangnai补贴.xlsx')
    # reward.to_excel(writer, index=False)
    # writer.save()
    # reward_sum = pd.pivot_table(reward, index=[r'员工编号'], values=[r'wongnai补贴'], aggfunc=np.sum)
    if len(reward) == 0:
        print('wongnai补贴！')
        return [dc_cr, pd.DataFrame([])]
    out = pd.merge(dc_cr, reward, left_on='员工编号', right_on='员工编号', how='left')
    out['wongnai补贴'] = out['wongnai补贴'].fillna(0)
    # 添加校验结果
    check = pd.DataFrame(
        {'原始字段': [r'wongnai补贴'], '原始数据汇总': [reward[r'wongnai补贴'].sum()], '提成数据汇总': [out[r'wongnai补贴'].sum()]})
    return [out, check]
