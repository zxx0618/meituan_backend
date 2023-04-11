# coding=utf-8
import pandas as pd
import numpy as np
import Integration.addin.add_integration as integra


# 生成DSCP待确认的文件格式***********************
def max_zero(d):  # 最终提成：若为负则改为0
    return (max(0, d[0] - d[1]))


def max_low(d):  # 最终提成：若为负则改为0
    return (max(d[0], d[1]))


def max_max(d):
    return (max(d[0], d[1]))


def rm_dcsp_dup(inv, rep):  # 去重：增值服务提成、复称奖励、buddy奖励、FDC、支援补贴、找场地奖励、疫情补贴、扣话费、补扣工资；

    if len(rep) == 0:  # 无重复
        return inv
    rep.insert(3, '去重', 0)
    inv = inv.fillna(0)
    inv = pd.merge(inv, rep, left_on='员工编号', right_on='员工编号', how='left')
    inv = inv.fillna(1)
    inv['增值服务提成'] = inv['增值服务提成'] * inv['去重']
    # inv['多发补扣'] = inv['多发补扣'] * inv['去重']
    inv['buddy奖励'] = inv['buddy奖励'] * inv['去重']
    inv['FDC'] = inv['FDC'] * inv['去重']
    inv['支援补贴'] = inv['支援补贴'] * inv['去重']
    # inv['找场地奖励'] = inv['找场地奖励'] * inv['去重']
    # inv['水果件提成'] = inv['水果件提成'] * inv['去重']
    inv['扣话费'] = inv['扣话费'] * inv['去重']
    inv['补扣工资'] = inv['补扣工资'] * inv['去重']
    # inv['内推奖励'] = inv['内推奖励'] * inv['去重']
    inv['CDC补贴'] = inv['CDC补贴'] * inv['去重']
    inv['芭提雅&普吉岛补贴'] = inv['芭提雅&普吉岛补贴'] * inv['去重']
    # inv['7&9&10月上报违规奖励'] = inv['7&9&10月上报违规奖励'] * inv['去重']

    #inv['拉新奖励'] = inv['拉新奖励'] * inv['去重']
    inv['平摊维修费用'] = inv['平摊维修费用'] * inv['去重']
    inv = inv.drop(columns=['提成类型_x', '提成类型_y', '去重'])
    # 重新计算
    if rep['提成类型_x'][0] == 'DC快递员提成':
        inv = integra.courier_intg(inv)
    else:  # 仓管员提成重算
        inv = integra.officer_intg(inv)
    return inv


def rm_hub_dup(inv, rep):  # 去重：复称奖励、疫情补贴、扣话费、补扣工资；

    if len(rep) == 0:  # 无重复
        return inv
    rep.insert(3, '去重', 0)
    inv = inv.fillna(0)
    inv = pd.merge(inv, rep, left_on='员工编号', right_on='员工编号', how='left')
    inv = inv.fillna(1)
    # inv['复称奖励'] = inv['复称奖励'] * inv['去重']
    # inv['疫情补贴'] = inv['疫情补贴'] * inv['去重']
    inv['扣话费'] = inv['扣话费'] * inv['去重']
    inv['补扣工资'] = inv['补扣工资'] * inv['去重']
    # inv['虚假扫描罚款'] = inv['虚假扫描罚款'] * inv['去重']
    inv = inv.drop(columns=['提成类型_x', '提成类型_y', '去重'])
    # 重新计算
    if rep['提成类型_x'][0] == 'DC快递员提成':
        inv = integra.courier_intg(inv)
    else:  # 仓管员提成重算
        inv = integra.officer_intg(inv)
    return inv


def rm_sup_dup(inv, rep):  # 主管去重:扣话费、补扣工资；
    if len(rep) == 0:  # 无重复
        return inv
    rep.insert(3, '去重', 0)
    inv = inv.fillna(0)
    inv = pd.merge(inv, rep, left_on='员工编号', right_on='员工编号', how='left')
    inv = inv.fillna(1)
    inv['扣话费'] = inv['扣话费'] * inv['去重']
    inv['补扣工资'] = inv['补扣工资'] * inv['去重']
    inv['虚假扫描罚款'] = inv['虚假扫描罚款'] * inv['去重']
    inv = inv.drop(columns=['提成类型_x', '提成类型_y', '去重'])
    inv = integra.supervisor_intg(inv)
    return inv


def rm_onsite_dup(inv, rep):  # 去除HUB和onsite之间的重复；全勤奖励	疫情补贴 扣话费 补扣工资
    if len(rep) == 0:  # 无重复
        return inv
    rep.insert(3, '去重', 0)
    inv = inv.fillna(0)
    inv = pd.merge(inv, rep, left_on='员工编号', right_on='员工编号', how='left')
    inv = inv.fillna(1)
    inv['全勤奖励'] = inv['全勤奖励'] * inv['去重']
    # inv['疫情补贴'] = inv['疫情补贴'] * inv['去重']
    inv['扣话费'] = inv['扣话费'] * inv['去重']
    inv['补扣工资'] = inv['补扣工资'] * inv['去重']
    inv = inv.drop(columns=['提成类型_x', '提成类型_y', '去重'])

    # 计算最终提成
    inv['实发提成'] = inv['当月应发提成 ฿'] + inv['全勤奖励'] - inv['包裹丢失'] \
                  - inv['包裹破损'] - inv['包裹丢失每件额外罚300thb'] - inv['扣话费'] - inv['补扣工资']
    inv['实发提成'] = inv[['全勤奖励', '实发提成']].apply(max_max, axis=1)

    return inv
