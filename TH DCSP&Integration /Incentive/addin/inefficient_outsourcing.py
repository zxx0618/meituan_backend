# coding=utf-8
import numpy as np
from Incentive.common_func import *
from Incentive.common_config import *


## 添加低效外协的数据
def inef_outsc(dc_cr, path, flist):  # 参数:提成数据,当前目录,目录下文件列表
    # 根据文件名读取文件，获取补助金额
    os.chdir(path)
    dexcel = ""
    for ex in flist:
        exx = ex.lower().strip()
        if exx.find('低效外协') > -1:
            dexcel = ex
            rdata = pd.read_excel(path + '/' + ex)
            ramout = rdata[[u"员工ID", '处罚金额']]
            # 筛选一下大于0的
            ramout = ramout.rename(columns={u"员工ID": '员工id', '处罚金额': '低效外协处罚'})
            # ramout = ramout[ramout['扣话费'] > 0]
            outcome = pd.pivot_table(ramout, index=['员工id'], values=['低效外协处罚'], aggfunc=np.sum)
            out = pd.merge(dc_cr, outcome, left_on='员工编号', right_on='员工id', how='left')
            out = out.fillna(0)
            # 添加校验结果
            check = pd.DataFrame(
                {'原始字段': ['低效外协处罚'], '原始数据汇总': [outcome[r'低效外协处罚'].sum()],
                 '提成数据汇总': [out[r'低效外协处罚'].sum()]})
            return [out, check]
    if dexcel == "":
        print('缺少：低效外协处罚的数据文件！')
        return [dc_cr, pd.DataFrame([])]
