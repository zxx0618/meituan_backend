# coding=utf-8
import pandas as pd
import numpy as np
import os

## 返回添加扣话费的数据
def phone_cost(dc_cr,path,flist):#参数:提成数据,当前目录,目录下文件列表
       #根据文件名读取文件，获取补助金额
       os.chdir(path)
       dexcel = ""
       for ex in flist:
              exx = ex.lower().strip()
              if exx.find('扣话费') > -1:
                     dexcel = ex
                     rdata= pd.read_excel(path+'/'+ex)
                     ramout=rdata[[u"Employee's ID",'Total except SMS (Baht)']]
                     #筛选一下大于0的
                     ramout=ramout.rename(columns={u"Employee's ID": '员工id','Total except SMS (Baht)':'扣话费'})
                     #ramout = ramout[ramout['扣话费'] > 0]
                     outcome = pd.pivot_table(ramout, index=['员工id'], values=['扣话费'], aggfunc=np.sum)
                     out = pd.merge(dc_cr, outcome, left_on='员工编号', right_on='员工id', how='left')
                     out = out.fillna(0)
                     check = pd.DataFrame(
                            {'原始字段': ['扣话费'], '原始数据汇总': [ramout[r'扣话费'].sum()],
                             '提成数据汇总': [out[r'扣话费'].sum()]})
                     return [out, check]
       if dexcel== "":
              print('缺少：扣话费的数据文件！')
              return  [dc_cr,pd.DataFrame([])]