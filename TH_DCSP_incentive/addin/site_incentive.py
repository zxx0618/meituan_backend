# coding=utf-8
import numpy as np
import pandas as pd
import os
from Incentive.common_func import *
from Incentive.common_config import *



## 返回添加找场地奖励的数据
def site_incentive(dc_cr, path, flist):  # 参数:提成数据,当前目录,目录下文件列表
    # 根据文件名读取文件，获取补助金额
    dexcel = ""
    for ex in flist:
        exx = ex.lower().strip()
        if exx.find('场地补助') > -1:
            dexcel = ex
            rdata = pd.read_excel(ex)
            ramout = rdata[['员工ID', '找场地奖励']]
            ramout = ramout.rename(columns={'员工ID': '员工id', '找场地奖励': '场地补助'})
            # outcome = pd.pivot_table(ramout, index=['员工id'], values=['场地补助'], aggfunc=np.sum)
            out = pd.merge(dc_cr, ramout, left_on='员工编号', right_on='员工id', how='left')
            out = out.fillna(0)
            out = out.drop(columns='员工id')
            # 添加校验结果
            check = pd.DataFrame(
                {'原始字段': ['场地补助'], '原始数据汇总': [ramout['场地补助'].sum()], '提成数据汇总': [out['场地补助'].sum()]})
            return [out, check]
    if dexcel == "":
        print('缺少：找场地奖励的数据文件！')
        return [dc_cr, pd.DataFrame([])]
