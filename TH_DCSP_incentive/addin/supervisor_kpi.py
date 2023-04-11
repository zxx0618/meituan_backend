# coding=utf-8
import pandas as pd
import numpy as np
import os


## 返回网点数据KPI
def supervisor_kpi(dc_cr, path, flist):  # 参数:提成数据,当前目录,目录下文件列表
    # 根据文件名读取文件，获取补助金额
    dexcel = ""
    for ex in flist:
        exx = ex.lower().strip()
        if exx.find('主管kpi') > -1:
            dexcel = ex
            rdata = pd.read_excel(ex)
            ramout = rdata[[u'Branch', '总分']]
            out = pd.merge(dc_cr, ramout, left_on='网点名称', right_on=u'Branch', how='left')
            out = out.fillna(100)
            out[r'本月网点正 / 副主管KPI得分'] = out[r'总分']
            out = out.drop(columns='总分')
            out = out.drop(columns=u'Branch')
            return out
    if dexcel == "":
        print('缺少：主管KPI的数据文件！')
        return dc_cr[r'本月网点正 / 副主管KPI得分']

# 返回仓管KPI
def officer_kpi(dc_cr, path, flist):  # 参数:提成数据,当前目录,目录下文件列表
    # 根据文件名读取文件，获取补助金额
    dexcel = ""
    for ex in flist:
        exx = ex.lower().strip()
        if exx.find('仓管kpi') > -1:
            dexcel = ex
            rdata = pd.read_excel(ex)
            ramout = rdata[[u'Branch', '总分']]
            out = pd.merge(dc_cr, ramout, left_on='网点名称', right_on=u'Branch', how='left')
            out = out.fillna(100)
            out[r'本月网点正 / 副主管KPI得分'] = out[r'总分']
            out = out.drop(columns='总分')
            out = out.drop(columns=u'Branch')
            out = out.rename(columns={'本月网点正 / 副主管KPI得分': '本月网点仓管KPI得分'})
            return out
    if dexcel == "":
        print('缺少：仓管KPI的数据文件！')
        return dc_cr[r'本月网点正 / 副主管KPI得分']

# def officer_kpi(dc_cr, path, flist):  # 参数:提成数据,当前目录,目录下文件列表
#     # 根据文件名读取文件，获取补助金额
#     os.chdir(path)
#     dexcel = ""
#     for ex in flist:
#         exx = ex.lower().strip()
#         if exx.find('仓管kpi') > -1:
#             dexcel = ex
#             rdata = pd.read_excel(ex)
#             ramout = rdata[[u"网点ID", 'KPI得分']]
#             # 筛选一下大于0的
#             # ramout = ramout.rename(columns={u"组长ID": '员工id', '总奖励': '组长补贴'})
#
#             # outcome = pd.pivot_table(ramout, index=['员工ID'], values=['芭提雅&普吉岛补贴'], aggfunc=np.sum)
#             out = pd.merge(dc_cr, ramout, left_on='网点', right_on='网点ID', how='left')
#             out = out.drop(columns='网点ID')
#             out = out.fillna(100)
#             return out
#     if dexcel == "":
#         print('缺少：芭提雅&普吉岛补贴的数据文件！')
#         return dc_cr[r'本月网点仓管KPI得分']