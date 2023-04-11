# coding=utf-8
import numpy as np
from Incentive.common_func import *
from Incentive.common_config import *

## 返回添加接驳补贴的数据
def link_incentive(dc_cr, path, flist):  # 参数:提成数据,当前目录,目录下文件列表
    # 根据文件名读取文件，获取补助金额
    os.chdir(path)
    dexcel = ""
    for ex in flist:
        exx = ex.lower().strip()
        if exx.find('接驳补贴') > -1:
            dexcel = ex
            rdata = pd.read_excel(path + '/' + ex)
            ramout = rdata[[u"员工ID", '补贴金额']]
            ramout = ramout.rename(columns={'员工ID':'员工编号','补贴金额': '接驳补贴'})
            outcome = pd.pivot_table(ramout, index=['员工编号'], values=['接驳补贴'], aggfunc=np.sum)
            out = pd.merge(dc_cr, outcome, left_on='员工编号', right_on='员工编号', how='left')
            out['接驳补贴'] = out['接驳补贴'].fillna(0)
            # 添加校验结果
            check = pd.DataFrame(
                {'原始字段': ['接驳补贴'], '原始数据汇总': [outcome[r'接驳补贴'].sum()],
                 '提成数据汇总': [out[r'接驳补贴'].sum()]})
            return [out, check]
    if dexcel == "":
        print('缺少：接驳补贴的数据文件！')
        return [dc_cr, pd.DataFrame([])]
