# coding=utf-8
import numpy as np
from Incentive.common_func import *
from Incentive.common_config import *


## 返回添加拉新奖励,流失客户挽回的奖励
def maintenance_reward(dc_cr, path, flist):  # 参数:提成数据,当前目录,目录下文件列表
    # 根据文件名读取文件，获取补助金额
    dexcel = ""
    for ex in flist:
        exx = ex.lower().strip()
        if exx.find('拉新奖励') > -1:
            dexcel = ex
            rdata = pd.read_excel(ex)
            ramout = rdata[['申请折扣员工id', '可获奖励（泰铢）']]
            ramout = ramout.rename(columns={'申请折扣员工id': '员工id', '可获奖励（泰铢）': '拉新奖励'})
            outcome = pd.pivot_table(ramout, index=['员工id'], values=['拉新奖励'], aggfunc=np.sum)
            out = pd.merge(dc_cr, outcome, left_on='员工编号', right_on='员工id', how='left')
            out = out.fillna(0)
            # 添加校验结果
            check = pd.DataFrame(
                {'原始字段': ['拉新奖励'], '原始数据汇总': [outcome[r'拉新奖励'].sum()],
                 '提成数据汇总': [out[r'拉新奖励'].sum()]})
            return [out, check]
    if dexcel == "":
        print('缺少：拉新奖励的数据文件！')
        return [dc_cr, pd.DataFrame([])]


def recommend_reward(dc_cr, path, flist):  # 参数:提成数据,当前目录,目录下文件列表
    # 根据文件名读取文件，推荐员工奖励
    dexcel = ""
    for ex in flist:
        exx = ex.lower().strip()
        if exx.find('招聘激励') > -1:
            dexcel = ex
            rdata = pd.read_excel(path + '/' + ex)
            ramout = rdata[['员工编号', '内推奖励']]
            ramout = pd.pivot_table(ramout, index=['员工编号'], values=['内推奖励'], aggfunc=np.sum)
            out = pd.merge(dc_cr, ramout, left_on='员工编号', right_on='员工编号', how='left')
            out = out.fillna(0)

            # 添加校验结果
            check = pd.DataFrame(
                {'原始字段': ['内推奖励'], '原始数据汇总': [ramout[r'内推奖励'].sum()],
                 '提成数据汇总': [out[r'内推奖励'].sum()]})
            return [out, check]
    if dexcel == "":
        print('缺少：内推奖励的数据文件！')
        return [dc_cr, pd.DataFrame([])]
