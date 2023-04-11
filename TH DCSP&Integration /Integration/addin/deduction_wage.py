# coding=utf-8
import pandas as pd
import numpy as np
import os

## 返回添加补扣工资的数据
def deduction_wage(dc_cr,path,flist):#参数:提成数据,当前目录,目录下文件列表
       #根据文件名读取文件，获取补助金额
       os.chdir(path)
       dexcel = ""
       for ex in flist:
              exx = ex.lower().strip()
              if exx.find('工资负数') > -1:
                     dexcel = ex
                     rdata= pd.read_excel(path+'/'+ex)
                     ramout=rdata[[u"Emp.",'Negative Data']]
                     ramout = ramout.rename(columns={u"Emp.":'员工id',u'Negative Data':'补扣工资'})
                     outcome = pd.pivot_table(ramout, index=[ramout.columns[0]], values=['补扣工资'], aggfunc=np.sum)
                     out = pd.merge(dc_cr, outcome, left_on='员工编号', right_on='员工id', how='left')
                     out = out.fillna(0)
                     return out
       if dexcel== "":
              print('缺少：补扣工资的数据文件！')
              return dc_cr