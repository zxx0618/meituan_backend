# coding=utf-8
import numpy as np
from Incentive.common_func import *
from Incentive.common_config import *


## 返回添加偏远地区补助的数据
def remote(dc_cr, path, flist):  # 参数:提成数据,当前目录,目录下文件列表
    # 根据文件名读取文件，获取补助金额
    dexcel = ""
    ramout = pd.DataFrame([], columns=['员工id', '补助金额'])
    for ex in flist:
        if ex.find('偏远地区补助') > -1:
            dexcel = ex
            rdata = pd.read_excel(ex)
            ramout = ramout.append(rdata[['员工id', '补助金额']])
    if dexcel == "":
        print('缺少：偏远地区补助的数据文件！')
        return dc_cr

    # 汇总数据并入提成
    if len(ramout) == 0:
        print('无偏远地区补助的数，请检查表头！\n\n\n！！！！')
    outcome = pd.pivot_table(ramout, index=['员工id'], values=['补助金额'], aggfunc=np.sum)
    out = pd.merge(dc_cr, outcome, left_on='员工编号', right_on='员工id', how='left')
    out = out.fillna(0)
    out = out.rename(columns={'补助金额': '偏远派件激励'})

    # 添加校验结果
    check = pd.DataFrame({'原始字段': ['偏远地区补助'], '原始数据汇总': [ramout['补助金额'].sum()], '提成数据汇总': [out['偏远派件激励'].sum()]})
    return [out, check]