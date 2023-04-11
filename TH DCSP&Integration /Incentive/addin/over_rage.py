# coding=utf-8
import numpy as np
from Incentive.common_func import *
from Incentive.common_config import *

## 临时处理，添加超发工资；
def over_wage(dc_cr,path,flist):#参数:提成数据,当前目录,目录下文件列表
       #根据文件名读取文件，获取补助金额
       # os.chdir(path)
       dexcel = ""
       for ex in flist:
              exx = ex.lower().strip()
              if exx.find('多发补扣') > -1:
                     dexcel = ex
                     rdata= pd.read_excel(path+'/'+ex)
                     ramout=rdata[[u"员工编号",'多发补扣']]
                     #ramout = ramout.rename(columns={u"Emp.":'员工id',u'Negative Data':'补扣工资'})
                     #outcome = pd.pivot_table(ramout, index=[ramout.columns[0]], values=['补扣工资'], aggfunc=np.sum)
                     out = pd.merge(dc_cr, ramout, left_on='员工编号', right_on='员工编号', how='left')
                     out = out.fillna(0)
                     # 添加校验结果
                     check =pd.DataFrame(
                            {'原始字段': ['多发补扣'], '原始数据汇总': [ramout[r'多发补扣'].sum()],
                             '提成数据汇总': [out[r'多发补扣'].sum()]})
                     return [out,check]
       if dexcel== "":
              print('缺少：超发工资的数据文件！')
              return  [dc_cr,pd.DataFrame([])]