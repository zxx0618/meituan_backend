# coding=utf-8
import numpy as np
from Incentive.common_func import *
from Incentive.common_config import *


## 返回添加驾照费用的数据
def driver_incentive(dc_cr, path, flist):  # 参数:提成数据,当前目录,目录下文件列表
    # 根据文件名读取文件，获取补助金额
    os.chdir(path)
    dexcel = ""
    for ex in flist:
        exx = ex.lower().strip()
        if exx.find('驾照') > -1:
            dexcel = ex
            rdata = pd.read_excel(path + '/' + ex)
            ramout = rdata[[u"MS ID", '总额']]
            ramout = ramout.rename(columns={u"MS ID": '员工id', '总额': '驾照补贴'})
            outcome = pd.pivot_table(ramout, index=['员工id'], values=['驾照补贴'], aggfunc=np.sum)
            out = pd.merge(dc_cr, outcome, left_on='员工编号', right_on='员工id', how='left')
            out = out.fillna(0)
            # 添加校验结果
            check = pd.DataFrame(
                {'原始字段': ['驾照补贴'], '原始数据汇总': [outcome[r'驾照补贴'].sum()],
                 '提成数据汇总': [out[r'驾照补贴'].sum()]})
            return [out, check]
    if dexcel == "":
        print('缺少：驾照费用的数据文件！')
        return [dc_cr, pd.DataFrame([])]
