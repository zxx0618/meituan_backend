# coding=utf-8
from Incentive.common_func import *


## 返回添加找场地奖励的数据
def buddy_incentive(dc_cr, path, flist):  # 参数:提成数据,当前目录,目录下文件列表
    # 根据文件名读取文件，获取补助金额
    dexcel = ""
    for ex in flist:
        exx = ex.lower().strip()
        if exx.find('辅导员') > -1:
            dexcel = ex
            rdata = pd.read_excel(ex)
            ramout = rdata[['Employee No.', 'Position']]
            ramout = ramout.rename(columns={'Employee No.': '员工id', 'Position': 'buddy奖励'})
            outcome = pd.pivot_table(ramout, index=[r'员工id'], values=['buddy奖励'], aggfunc='count')
            outcome['buddy奖励'] = outcome['buddy奖励'] * 500
            out = pd.merge(dc_cr, outcome, left_on='员工编号', right_on='员工id', how='left')
            out = out.fillna(0)
            # 添加校验结果
            check = pd.DataFrame(
                {'原始字段': ['Buddy奖励'], '原始数据汇总': [outcome['buddy奖励'].sum()], '提成数据汇总': [out['buddy奖励'].sum()]})
            return [out, check]
    if dexcel == "":
        print('缺少：buddy辅导员奖励的数据文件！')
        return [dc_cr, pd.DataFrame([])]
