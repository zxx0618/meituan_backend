# coding=utf-8
import numpy as np
from Incentive.common_func import *
from Incentive.common_config import *


## 添加快递员虚报油卡里程
def oil_kilometres(dc_cr, path, flist):  # 参数:提成数据,当前目录,目录下文件列表
    # 规则：
    # 1.状态是通过：（负数）应补/（正数）应扣提成 若为负数，则补油卡；若为正数，则扣提成；
    # 2.状态是模糊：若注明不给予补回，则按0；若注明口头警告，则（负数）应补/（正数）应扣提成 若为负数，则补油卡，若为正数，则扣提成；
    # 3.状态是虚假：若注明不给予补回，则按0；若注明口头警告，则（负数）应补/（正数）应扣提成 若为负数，则补油卡，若为正数，则扣提成；
    # 4.状态是未审核和审核中：不予处理
    # 5.状态是模糊和虚假，并且没有标注的：应扣的扣除，应补的不予处理；该项规则一般不会出现；

    # 根据文件名读取文件，获取补助金额
    dexcel = ""
    for ex in flist:
        if ex.find('油卡里程') > -1:
            dexcel = ex
            rdata = pd.read_excel(ex)
            # shenhe = rdata[rdata['WRS审核状态สถานะการตรวจ'] == '通过ผ่าน']
            shenhe = rdata.rename(columns={u'工号': '员工工号',u'油补': '补发油卡'})
            shenhe_sum = pd.pivot_table(shenhe, index=[u'员工工号'], values=[u'补发油卡'], aggfunc=np.sum)
            shenhe_sum['补发油卡'] = -1 * shenhe_sum[u'补发油卡']
            out = pd.merge(dc_cr, shenhe_sum, left_on='员工编号', right_on='员工工号', how='left')
            # 添加校验结果
            check = pd.DataFrame(
                {'原始字段': ['补发油卡'], '原始数据汇总': [shenhe_sum['补发油卡'].sum()],
                 '提成数据汇总': [out['补发油卡'].sum()]})

            # xubao = rdata[rdata['WRS审核状态สถานะการตรวจ'] == '模糊เบลอ']
            # xubao = xubao.append(rdata[rdata['WRS审核状态สถานะการตรวจ'] == '虚假เท็จ'])
            # xubao = xubao[(xubao['Status'].str.contains('不给予补回') != True)]
            # xubao = xubao.rename(columns={u'员工工号รหัสพนักงาน': '员工工号',
            #                               u'（负数）应补/（正数）应扣提成(THB) เลขติดลบต้องทำการคืนเงิน/เลขบวกต้องหักจากค่าคอม': '虚报油卡'})
            # if len(xubao) > 0:  # 防止没有数据
            #     xubao_sum = pd.pivot_table(xubao, index=[u'员工工号'], values=[u'虚报油卡'], aggfunc=np.sum)
            #     xubao_sum['虚报油卡'] = -1 * xubao_sum['虚报油卡']
            #     out = pd.merge(out, xubao_sum, left_on='员工编号', right_on='员工工号', how='left')
            #     check = check.append(pd.DataFrame(
            #         {'原始字段': ['虚报油卡'], '原始数据汇总': [xubao_sum['虚报油卡'].sum()],
            #          '提成数据汇总': [out['虚报油卡'].sum()]}))

            # out = out.fillna(0)
            return [out, check]
    if dexcel == "":
        print('缺少：快递员虚报油卡里程的数据文件！')
        return [dc_cr, pd.DataFrame([])]
