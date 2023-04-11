# coding=utf-8
import numpy as np
from Incentive.common_func import *
from Incentive.common_config import *

## 返回添加水果件提成的数据
def fruit_reward(dc_cr,path,flist):#参数:提成数据,当前目录,目录下文件列表
       #直接读取数据库

       SQL="""
        SELECT cast(ffd.give_id as int) 员工编号,
              #COUNT(ffd.`give_id`) 水果件数,
              sum(ffd.amount) 水果件提成
         FROM `nl_production`.`finance_fruit_detail` ffd
         left join `fle_staging`.sys_store ss on ss.id= ffd.store_id
         LEFT JOIN `bi_pro`.`hr_staff_info_%s` hsi on hsi.`staff_info_id`= ffd.`give_id`
         left join `bi_pro`.`sys_department` sd on sd.`id`= hsi.`sys_department_id`
        where ffd.stat_date>= CURRENT_DATE - INTERVAL day(CURRENT_DATE) -1 day -INTERVAL 1 month
          and ffd.stat_date< CURRENT_DATE - INTERVAL day(CURRENT_DATE) -1 day
          and hsi.sys_department_id in (4, 34)
        GROUP BY give_id
       """
       mm = str(datetime.date.today() - datetime.timedelta(days=31))
       mm = (mm[0:4] + mm[5:7])
       SQL = SQL % mm
       engine_ads = create_engine(engine_info_ads)
       # 从数据库读取结果为dataframe
       reward = pd.read_sql(SQL, engine_ads)
       engine_ads.dispose()
       writer = pd.ExcelWriter(path+'/02.水果件提成.xlsx')
       reward.to_excel(writer, index=False)
       writer.save()
       writer.close()
       out = pd.merge(dc_cr, reward, left_on='员工编号', right_on='员工编号', how='left')
       out = out.fillna(0)
       # 添加校验结果
       if len(reward)>0:
              check = pd.DataFrame({'原始字段': ['水果件提成'], '原始数据汇总': [ reward[r'水果件提成'].sum()], '提成数据汇总': [out['水果件提成'].sum()]})
       else:
              check = pd.DataFrame([])
       return [out,check]
