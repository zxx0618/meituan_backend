# coding=utf-8
import numpy as np
from Incentive.common_func import *


## 这里对数据进行整合，将罚款项进行合并；将这些函数独立出来是为了去重；

def max_zero(d):
    return (max(0, d[0] - d[1]))


def no_deduct(d):  # 默认与第一项进行比较
    reward = sum(d) - d[0]
    return round(max(d[0], reward), 2)


def courier_intg(dc_cr):  # 快递员的整合
    idxs = (np.where(dc_cr.columns == '本月提成金额฿'))[0][0]
    idxe = (np.where(dc_cr.columns == '提成应发放金额฿'))[0][0]
    dc_cr['提成应发放金额฿'] = dc_cr.iloc[:, idxs:idxe].apply(np.sum, axis=1)
    penalty_columns = ['虚假问题件 / 虚假留仓件罚款',
                       '揽件时称量包裹不准确罚款',
                       '包裹丢失罚款',
                       '包裹破损罚款',
                       'PRI件/SPEED件未妥投包裹罚款',
                       '公款超时未上缴罚款',
                       '客户投诉罚款',
                       '客户投诉--虚假问题件/虚假留仓件罚款',
                       '虚假妥投包裹罚款',
                       '故意不接公司电话罚款',
                       '迟到罚款',
                       '工单处理不及时罚款',
                       '5天内未妥投/未中转，且超过一天未更新包裹罚款',
                       '5天外未妥投/未中转，且超过一天未更新包裹罚款',
                       'minics对问题件解决不及时罚款',
                       'miniCS对工单处理不及时罚款',
                       '揽收或中转包裹未及时发出包裹罚款',
                       '仓管未及时处理问题件包裹罚款',
                       '仓管未及时交接speed/优先包裹罚款',
                       '揽收禁运包裹罚款',
                       '早退罚款',
                       '班车发车晚点',
                       '未妥投包裹没有标记罚款',
                       '未妥投包裹没有入仓罚款',
                       '揽收任务超时罚款',
                       '虚假上报罚款',
                       '其他',
                       '平摊维修费用',
                       '扣话费',
                       '补扣工资',
                       '多发补扣'
                       # '虚假扫描罚款'
                       ]
    dc_cr['快递员当月罚款合计'] = dc_cr[penalty_columns].apply(np.sum, axis=1)

    diff_columns = ['提成应发放金额฿', '快递员当月罚款合计']
    dc_cr['快递员当月应发放提成金额฿'] = dc_cr[diff_columns].apply(max_zero, axis=1)
    dc_cr['快递员当月应发放提成金额฿'] = dc_cr[['快递员当月应发放提成金额฿',  'buddy奖励','芭提雅&普吉岛补贴',
                                    '驾照补贴', '支援补贴', 'wongnai补贴','人效补贴','场地补助']].apply(no_deduct, axis=1)  # 不减扣项；
    # dc_cr['快递员当月应发放提成金额฿'] = dc_cr[['快递员当月应发放提成金额฿', '多发补扣']].apply(max_zero, axis=1)
    return dc_cr


def officer_intg(dc_of):  # 仓管员的整合
    idxs = (np.where(dc_of.columns == '应发奖金池'))[0][0]
    idxe = (np.where(dc_of.columns == '本月提成金额฿'))[0][0]
    dc_of['本月提成金额฿'] = dc_of.iloc[:, idxs:idxe].apply(np.sum, axis=1)
    penalty_columns = ['虚假问题件 / 虚假留仓件罚款',
                       '揽件时称量包裹不准确罚款',
                       '虚假上报罚款',
                       '包裹丢失罚款',
                       '包裹破损罚款',
                       'PRI件/SPEED件未妥投包裹罚款',
                       '公款超时未上缴罚款',
                       '客户投诉罚款',
                       '客户投诉--虚假问题件/虚假留仓件罚款',
                       '虚假妥投包裹罚款',
                       '故意不接公司电话罚款',
                       '迟到罚款',
                       '工单处理不及时罚款',
                       '5天内未妥投/未中转，且超过一天未更新包裹罚款',
                       '5天外未妥投/未中转，且超过一天未更新包裹罚款',
                       'minics对问题件解决不及时罚款',
                       'miniCS对工单处理不及时罚款',
                       '揽收或中转包裹未及时发出包裹罚款',
                       '仓管未及时处理问题件包裹罚款',
                       '仓管未及时交接speed/优先包裹罚款',
                       '揽收禁运包裹罚款',
                       '早退罚款',
                       '班车发车晚点',
                       '未妥投包裹没有标记罚款',
                       '未妥投包裹没有入仓罚款',
                       '揽收任务超时罚款',
                       '其他',
                       '平摊维修费用'
                       ]
    # 罚款款使用揽件人效系数调整
    dc_of['个人罚款合计'] = dc_of[penalty_columns].apply(np.sum, axis=1)
    # dc_of['个人罚款合计调整'] = dc_of['个人罚款合计']
    dc_of['个人扣款合计'] = dc_of['个人罚款合计'] + dc_of['扣话费'] + dc_of['补扣工资'] + dc_of['低效外协处罚'] # + dc_of['虚假扫描罚款']
    dc_of['本月提成金额฿'] = dc_of['应发奖金池'] + dc_of['本月推荐客户发件提成'] + dc_of['FD_OT'] + \
                       dc_of['增值服务提成'] + dc_of['违规件举报奖励'] + dc_of['buddy奖励']  \
                       + dc_of['FDC'] + dc_of['支援补贴']  + dc_of['错分包裹补贴'] + dc_of['揽收称重不准确复称奖励'] + \
                       dc_of['场地补助']+ dc_of['CDC补贴'] + dc_of['大件操作补贴']  + dc_of['芭提雅&普吉岛补贴']

    dc_of['本月应发放提成฿'] = dc_of[['本月提成金额฿', '个人扣款合计']].apply(max_zero, axis=1)
    dc_of['本月应发放提成฿'] = dc_of[['本月应发放提成฿', 'buddy奖励','场地补助','芭提雅&普吉岛补贴',
                               '支援补贴']].apply(no_deduct, axis=1)  # 不减扣项；
    # dc_of['本月应发放提成฿'] = dc_of[['本月应发放提成฿', '多发补扣']].apply(max_zero, axis=1)
    return dc_of


def supervisor_intg(sup):  # 主管的整合
    idxs = int(np.where(sup.columns == r'本月网点正 / 副主管KPI得分')[0]) + 1
    idxd = int(np.where(sup.columns == r'本月提成金额฿')[0])
    sup['本月提成金额฿'] = sup.iloc[:, idxs:idxd].apply(np.sum, axis=1)

    penalty_columns = [
        '个人罚款合计',
        '低效外协处罚',
        '平摊维修费用',
        '扣话费',
        '补扣工资'
        # '多发补扣'
        # '虚假扫描罚款'

    ]
    sup['个人扣款合计'] = sup[penalty_columns].apply(np.sum, axis=1)
    diff_columns = [u'本月提成金额฿', '个人扣款合计']
    sup['本月应发放提成฿'] = sup[diff_columns].apply(max_zero, axis=1)
    sup['本月应发放提成฿'] = sup[['本月应发放提成฿', 'buddy奖励', '支援补贴','场地补助','芭提雅&普吉岛补贴']].apply(no_deduct, axis=1)  # 不减扣项；
    # sup[u'本月应发放提成฿'] = sup[['本月应发放提成฿', '多发补扣']].apply(max_zero, axis=1)
    return sup
