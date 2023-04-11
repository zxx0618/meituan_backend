# coding=utf-8
import numpy as np
from Incentive.common_func import *
from Incentive.common_config import *

## 返回添加中心区域的50%派件补贴
def keeper_ratio(dc_cr,path,flist):#参数:提成数据,当前目录,目录下文件列表
       #直接读取数据库
       # path = os.getcwd()
       # os.chdir(path)
       SQL="""
       SELECT  fca.`staff_info_id` 员工编号,
              min(fca.keeper_ratio) `揽件人效系数`
         from `bi_pro`.`finance_keeper_manager_month` fca
        where fca.`stat_date`>= CURRENT_DATE - INTERVAL day(CURRENT_DATE) -1 day -INTERVAL 1 month
          and fca.`stat_date`< CURRENT_DATE - INTERVAL day(CURRENT_DATE) -1 day
          group by 1
       """

       engine_ads = create_engine(engine_info_ads)
       # 从数据库读取结果为dataframe
       reward = pd.read_sql(SQL, engine_ads)
       engine_ads.dispose()
       out = pd.merge(dc_cr, reward , left_on='员工编号', right_on='员工编号', how='left')
       out = out.fillna(0)
       return out

