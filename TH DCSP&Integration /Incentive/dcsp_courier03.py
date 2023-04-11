# coding=utf-8
import numpy as np
from common_func import *
from raw_dir import *
# 以下为自定义函数
import addin.remote_amount as remote_amout
import addin.oil_kilometres as oil_kilometres
import addin.reweight_reward as reweight_reward
import addin.site_incentive as site_incentive
import addin.center_attendance as center_attendance
import addin.center_incentive as center_incentive
import addin.buddy_incentive as buddy_incentive
import addin.fdc_incentive as FDC_incentive
import addin.driver_incentive as driver_incentive
import addin.support_incentive as support_incentive
import addin.phone_cost as phone_cost
import addin.deduction_wage as deduction_wage
import addin.add_integration as integra
import addin.over_rage as over_wage
import addin.fruit_reward as fruit
import addin.damage_device as damage_device
import addin.maintenance_reward as maintenance_reward
import addin.link_incentive as link_incentive
import addin.wongnai_reward as wongnai_reward
import addin.cdc_reward as cdc_reward
import addin.false_scan_penalty as false_scan_penalty

## 设置工作路径,提成文件所在的路径,以及输出路径
os.chdir(path)
if os.path.isdir(output) == False:
    os.makedirs(output)

# 找到快递员提成的文件================================================
flist = os.listdir()
dexcel = ""
for ex in flist:
    if ex.find('dc_finance_merge_courier') > -1:
        dexcel = ex
if not os.path.exists(dexcel):
    print('缺少：提成数据文件！')
    quit()
## 导入数据，并筛选出快递员
dc_courier = pd.read_excel(dexcel)

# #筛选出boat courier，求和并简单保存====================================
boat_courier = dc_courier[dc_courier['职位'] == 'Boat Courier']
boat_courier = boat_courier.drop(columns=boat_courier.columns[(int(np.where(dc_courier.columns == '本月推荐客户发件提成')[0])):])
collist = list(boat_courier)[11:]
#添加 人效达成奖励 20221010
# [boat_courier, ck] = support_incentive.OLE_incentive(boat_courier, path, flist)

boat_courier['本月提成金额฿'] = boat_courier[collist].apply(np.sum, axis=1)
boat_courier = boat_courier.drop(columns='该员工提成计算规则')
boat_courier = boat_courier.drop(columns='网点类型')
boatfile = pd.ExcelWriter(output + '00.本月提成结果_boatcourier.xlsx')
boat_courier.to_excel(boatfile, sheet_name='dc_boatcourier', index=False)
boatfile.save()
print('00.boat_courier计算完成')

##筛选出dc courier和罚款项：提成应发放金额฿列之后及最后一列之前============
dc_courier = dc_courier[dc_courier['职位'] != 'Boat Courier']
penalty = dc_courier.iloc[:, (int(np.where(dc_courier.columns == '提成应发放金额')[0]) + 1):-1]
penalty['员工编号'] = dc_courier['员工编号']
# 筛选出每日奖励池
dc_cr = dc_courier.drop(columns=dc_courier.columns[(int(np.where(dc_courier.columns == '本月推荐客户发件提成')[0])):])
## 核对 奖金池合计
collist = list(dc_cr)[11:]
dc_cr['本月提成金额฿'] = dc_cr[collist].apply(np.sum, axis=1)
dc_cr['增值服务提成'] = dc_courier['增值服务提成']

# #偏远地区派件激励******************
[dc_cr, check] = remote_amout.remote(dc_cr, path, flist)
print('01.偏远地区派件激励计算完成')
# 补发里和和油卡*********************
[dc_cr, ck] = oil_kilometres.oil_kilometres(dc_cr, path, flist)
check = check.append(ck)
print('02.补发里和和油卡计算完成')
# 复称奖励*************************
[dc_cr, ck] = reweight_reward.reweight_reward(dc_cr, path, flist)
check = check.append(ck)
print('03.复称奖励计算完成')
##
[dc_cr, ck] = site_incentive.site_incentive(dc_cr, path, flist)
check = check.append(ck)
print('04.场地补贴计算完成')
# [dc_cr, ck] = center_attendance.center_attendance(dc_cr, path, flist)
# check = check.append(ck)
# print('05.中心区域的出勤补贴计算完成')
# 派件50%补贴*************************
[dc_cr, ck] = center_incentive.center_incentive(dc_cr, path, flist)
check = check.append(ck)
print('05.派件50%补贴计算完成')
[dc_cr, ck] = buddy_incentive.buddy_incentive(dc_cr, path, flist)
check = check.append(ck)
print('06.buddy奖励计算完成')
[dc_cr, ck] = FDC_incentive.FDC_incentive(dc_cr, path, flist)
check = check.append(ck)
print('07.FDC奖励计算完成')
[dc_cr, ck] = driver_incentive.driver_incentive(dc_cr, path, flist)
check = check.append(ck)
print('08.驾照费用补贴计算完成')
[dc_cr, ck] = support_incentive.support_courierV2(dc_cr, path, flist)
check = check.append(ck)
print('09.支援补贴计算完成')
# [dc_cr, ck] = fruit.fruit_reward(dc_cr, path, flist)
# check = check.append(ck)
# print('10.水果件计算完成')
## 内推奖励*************************
# [dc_cr, ck] = maintenance_reward.recommend_reward(dc_cr, path, flist)
# check = check.append(ck)
# print('10.内推奖励计算完成')
## 接驳补贴*************************
[dc_cr, ck] = link_incentive.link_incentive(dc_cr, path, flist)
check = check.append(ck)
print('11.接驳补贴计算完成')
## 人效达成奖*************************
[dc_cr, ck] = support_incentive.OLE_incentive(dc_cr, path, flist)
check = check.append(ck)
print('12.人效补贴计算完成')

# 组长补贴*******************************
[dc_cr,ck] = support_incentive.leader_subsidy(dc_cr,path,flist)
check = check.append(ck)
print('13.组长补贴计算完成')

## 芭提雅&普吉岛补贴*************************
[dc_cr, ck] = support_incentive.Pattaya_Phuket_Subsidy(dc_cr, path, flist)
check = check.append(ck)
print('14.芭提雅&普吉岛补贴计算完成')

## wongnai_reward*************************
[dc_cr, ck] = wongnai_reward.wongnai_reward(dc_cr, path, flist)
check = check.append(ck)
print('15.wongnai_reward计算完成')

## CDC月度补贴*************************
[dc_cr, ck] = cdc_reward.cdc_reward(dc_cr, path, flist)
check = check.append(ck)
print('16.CDC月度补贴计算完成')

## 曼谷和东部区域特殊补贴 -- 快递员
[dc_cr, ck] = support_incentive.Bangkok_special_subsidy(dc_cr, path, flist)
check = check.append(ck)
print('17.曼谷和东部区域特殊补贴计算完成')


## 出勤补贴 -- 快递员
[dc_cr, ck] = support_incentive.attendance_subsidy(dc_cr, path, flist)
check = check.append(ck)
print('18.出勤补贴计算完成')


# 7&9&10月上报违规奖励
# [dc_cr, ck] = support_incentive.violation_reward(dc_cr, path, flist)
# check = check.append(ck)
# print('17.7&9&10月上报违规奖励计算完成')


# 以下为罚款项目计算-------------------------------------
[penalty, ck] = phone_cost.phone_cost(penalty, path, flist)
check = check.append(ck)
print('17.补扣话费计算完成')
[penalty, ck] = deduction_wage.deduction_wage(penalty, path, flist)
check = check.append(ck)
print('18.补扣工资计算完成')
[penalty, ck] = damage_device.damage_device(penalty, path, flist)
check = check.append(ck)
print('19.平摊维修费用计算完成')
[penalty, ck] = over_wage.over_wage(penalty, path, flist)
check = check.append(ck)
print('20.多发补扣计算完成')
# 虚假扫描罚款 替补
# [penalty, ck] = false_scan_penalty.false_scan_penalty(penalty, path, flist)
# check = check.append(ck)
# print('21.虚假扫描罚款计算完成')

# 以下进行数据整合-*****************************************
idxs = (np.where(dc_cr.columns == '本月提成金额฿'))[0][0]
dc_cr['提成应发放金额฿'] = dc_cr.iloc[:, idxs:].apply(np.sum, axis=1)
dc_cr = pd.merge(dc_cr, penalty, how='left', left_on='员工编号', right_on='员工编号')
# 提成数据整合
dc_cr = integra.courier_intg(dc_cr)

dc_cr = dc_cr.drop(columns='该员工提成计算规则')
dc_cr = dc_cr.drop(columns='网点类型')
current_month = pd.ExcelWriter(output + '00.本月提成结果_courier.xlsx')
# boatfile = pd.ExcelWriter(output + '00.本月提成结果_boatcourier.xlsx')
dc_cr.to_excel(current_month, sheet_name='dc_courier', index=False)
current_month.save()
print('98.courier提成计算完成并保存')

# 添加校验结果
check = check.append(pd.DataFrame({'原始字段': ['每日提成合计'],
                                   '原始数据汇总': [dc_courier['提成应发放金额'].sum() - dc_courier['FD_OT'].sum() - dc_courier[
                                       '违规件举报奖励'].sum()],
                                   '提成数据汇总': [dc_cr['本月提成金额฿'].sum() + dc_cr['增值服务提成'].sum()]}))
# 罚款数据校验
check = check.append(pd.DataFrame({'原始字段': ['快递员当月罚款合计'], '原始数据汇总': [dc_courier['快递员当月罚款合计'].sum()],
                                   '提成数据汇总': [penalty['快递员当月罚款合计'].sum()]}))
# 汇总校验
check = check.append(pd.DataFrame({'原始字段': ['汇总校验参考'], '原始数据汇总': [dc_cr['本月提成金额฿'].sum() - dc_cr['快递员当月罚款合计'].sum()],
                                   '提成数据汇总': [dc_cr['快递员当月应发放提成金额฿'].sum()]}))
today = str(get_current_date())
checkWriter = pd.ExcelWriter(output + '01.courier校验结果' + str(get_current_date()) + '.xlsx')
check.to_excel(checkWriter, sheet_name='dc_courier', index=False)
checkWriter.save()

print('97.courier校验结果已保存\n')
