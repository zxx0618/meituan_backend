# coding=utf-8
import pandas as pd
import numpy as np
import os


## 返回添加扣话费的数据
def cdc_reward(dc_cr, path, flist):  # 参数:提成数据,当前目录,目录下文件列表
    # 根据文件名读取文件，获取补助金额
    os.chdir(path)
    dexcel = ""
    for ex in flist:
        exx = ex.lower().strip()
        if exx.find('cdc月度补贴') > -1:
            dexcel = ex
            rdata = pd.read_excel(path + '/' + ex)
            ramout = rdata[[u"员工ID", 'cdc月度补贴']]
            # 筛选一下大于0的
            ramout = ramout.rename(columns={u"员工ID": '员工编号', 'cdc月度补贴': 'CDC补贴'})
            # ramout = ramout[ramout['扣话费'] > 0]
            outcome = pd.pivot_table(ramout, index=['员工编号'], values=['CDC补贴'], aggfunc=np.sum)
            out = pd.merge(dc_cr, outcome, left_on='员工编号', right_on='员工编号', how='left')
            out['CDC补贴'] = out['CDC补贴'].fillna(0)
            check = pd.DataFrame(
                {'原始字段': ['CDC补贴'], '原始数据汇总': [ramout[r'CDC补贴'].sum()],
                 '提成数据汇总': [out[r'CDC补贴'].sum()]})
            return [out, check]
    if dexcel == "":
        print('缺少：CDC补贴的数据文件！')
        return [dc_cr, pd.DataFrame([])]
