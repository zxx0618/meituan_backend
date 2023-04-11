# coding=utf-8
import pandas as pd
import numpy as np
import os


## 低提成补贴处理；
def low_subsidy(dc_of, dc_sup, path, flist):  # 参数:提成数据,当前目录,目录下文件列表
    os.chdir(path)
    dexcel = ""
    for ex in flist:
        exx = ex.lower().strip()
        if exx.find('低提成') > -1 and ex.find('~') == -1:
            dexcel = ex
            lowoff = pd.read_excel(path + '/' + ex, sheet_name='仓管提成小于500泰铢')
            lowsup = pd.read_excel(path + '/' + ex, sheet_name='主管提成1000泰铢')
            lowoff = lowoff[[u"员工编号", '最终应发放提成金额']]
            lowsup = lowsup[[u"员工编号", '最终应发放提成金额']]

            out_of = pd.merge(dc_of, lowoff, left_on='员工编号', right_on='员工编号', how='left')
            out_of['最终应发放提成金额'] = out_of['最终应发放提成金额'].fillna(0)
            out_of['本月应发放提成฿'] = out_of[['本月应发放提成฿', '最终应发放提成金额']].apply(max, axis=1)
            out_of = out_of.drop(columns='最终应发放提成金额')

            out_sup = pd.merge(dc_sup, lowsup, left_on='员工编号', right_on='员工编号', how='left')
            out_sup['最终应发放提成金额'] = out_sup['最终应发放提成金额'].fillna(0)
            out_sup['本月应发放提成฿'] = out_sup[['本月应发放提成฿', '最终应发放提成金额']].apply(max, axis=1)
            out_sup = out_sup.drop(columns='最终应发放提成金额')
    if dexcel == "":
        print('缺少：低提成补贴的数据文件！')
        return [dc_of, dc_sup]
    else:
        return [out_of, out_sup]
