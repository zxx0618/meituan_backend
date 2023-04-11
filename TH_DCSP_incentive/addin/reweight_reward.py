# coding=utf-8
import numpy as np
from Incentive.common_func import *
from Incentive.common_config import *

## 返回添加复称奖励的数据
def reweight_reward(dc_cr,path,flist):#参数:提成数据,当前目录,目录下文件列表
       #直接读取数据库
       # path = os.getcwd()
       # os.chdir(path)
       SQL="""
       SELECT `reward_staff_info_id` 员工编号,
              `reward_money` 复称奖励,
              `abnormal_time`
         FROM `bi_pro`.`abnormal_message` am
        where `punish_category`= 10
          and `abnormal_time`>= CURRENT_DATE - INTERVAL day(CURRENT_DATE) -1 day -INTERVAL 1 month
          and `abnormal_time`< CURRENT_DATE - INTERVAL day(CURRENT_DATE) -1 day
          and `isdel`= 0
          and `reward_staff_info_id` is not null
       """

       engine_ads = create_engine(engine_info_ads)
       # 从数据库读取结果为dataframe
       reward = pd.read_sql(SQL, engine_ads)
       engine_ads.dispose()
       writer = pd.ExcelWriter(path+'/02.复称奖励.xlsx')
       reward.to_excel(writer, index=False)
       writer.save()
       reward_sum=pd.pivot_table(reward, index=[u'员工编号'], values=[u'复称奖励'], aggfunc=np.sum)
       out = pd.merge(dc_cr, reward_sum, left_on='员工编号', right_on='员工编号', how='left')
       out = out.fillna(0)
       # 添加校验结果
       if len(reward)>0:
              check = pd.DataFrame({'原始字段': ['复称奖励'], '原始数据汇总': [ reward_sum[r'复称奖励'].sum()], '提成数据汇总': [out['复称奖励'].sum()]})
       else:
              check = pd.DataFrame([])
       return [out,check]
