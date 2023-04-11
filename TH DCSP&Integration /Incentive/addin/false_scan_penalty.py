# coding=utf-8
import pandas as pd
import numpy as np
import os


## 返回添加补扣工资的数据
def false_scan_penalty(dc_cr, path, flist):  # 参数:提成数据,当前目录,目录下文件列表
    # 根据文件名读取文件，获取补助金额
    os.chdir(path)
    dexcel = ""
    for ex in flist:
        exx = ex.lower().strip()
        if exx.find('虚假扫描罚款') > -1:
            dexcel = ex
            rdata = pd.read_excel(path + '/' + ex)
            ramout = rdata[[u"员工ID", '虚假扫描罚款']]
            ramout = ramout.rename(columns={u"员工ID": '员工id'})
            outcome = pd.pivot_table(ramout, index=[ramout.columns[0]], values=['虚假扫描罚款'], aggfunc=np.sum)
            out = pd.merge(dc_cr, outcome, left_on='员工编号', right_on='员工id', how='left')
            out = out.fillna(0)
            # 添加校验结果
            check = pd.DataFrame(
                {'原始字段': ['虚假扫描罚款'], '原始数据汇总': [ramout['虚假扫描罚款'].sum()],
                 '提成数据汇总': [out['虚假扫描罚款'].sum()]})
            return [out, check]
    if dexcel == "":
        print('缺少：虚假扫描罚款的数据文件！')
        return [dc_cr, pd.DataFrame([])]
