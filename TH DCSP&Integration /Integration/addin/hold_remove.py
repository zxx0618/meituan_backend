# coding=utf-8
import pandas as pd
import numpy as np
import os

## 删除法院扣款和HOLD数据
# class remove_hold():
#        def __init__(self, path, flist):#参数:当前目录,目录下文件列表
#               dexcel = 0
#               self.rm['HOLD']='0'
#               for ex in flist:
#                      exx = ex.lower().strip()
#                      if exx.find('法院扣款') > -1:
#                             dexcel =dexcel+ 1
#                             court= pd.read_excel(path+'/'+ex)
#                             self.rm.append(court['MS'])
#                             print('读取法院扣款')
#                      if exx.find('提成hold') > -1:
#                             dexcel =dexcel+ 1
#                             hold= pd.read_excel(path+'/'+ex)
#                             self.rm.append(hold['Employee No.'])
#                             print('读取HOLD数据')
#               self.rm=self.rm[self.rm!='0']
#               if dexcel== 0:
#                      print('缺少：HOLD数据文件！')
#
#        def rm_hold(self,inv,inx):
#               inv=pd.merge(inv, self.rm, left_on=inx, right_on='hold', how='left')
#               inv =inv[inv['hold']!=np.nan]
#               inv.drop(columns = 'hold')
#               return inv

def rm_hold(inv,hold):
       inv = pd.merge(inv, hold, left_on='员工编号', right_on='hold', how='left')
       inv = inv[inv['hold'].isna()]
       inv = inv.drop(columns = 'hold')
       return inv
