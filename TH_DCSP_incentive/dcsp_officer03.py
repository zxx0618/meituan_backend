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
import addin.inefficient_outsourcing as inef_outsc
import addin.keeper_ratio as keeper_ratio
import addin.over_rage as over_wage
import addin.add_integration as integra
import addin.fruit_reward as fruit
import addin.damage_device as damage_device
import addin.maintenance_reward as maintenance_reward
import addin.cdc_reward as cdc_reward
import addin.supervisor_kpi as supervisor_kpi
import addin.false_scan_penalty as false_scan_penalty


## 设置工作路径
if os.path.isdir(output) == False:
    os.makedirs(output)
os.chdir(path)

## 导入数据
flist = os.listdir()
dexcel = ""
for ex in flist:
    if ex.find('merge_managerkeeper') > -1:
        dexcel = ex
if not os.path.exists(dexcel):
    print('缺少：提成数据文件！')
    quit()
## 导入数据，并筛选出仓管员 和罚款项
dc_officier = pd.read_excel(dexcel)
dc_officier = dc_officier[dc_officier['该员工提成计算规则'].str.contains('仓管员') == True]

dc_of = dc_officier.drop(columns=dc_officier.columns[int(np.where(dc_officier.columns == '本月提成金额')[0]):])

penalty = dc_officier.iloc[:, (int(np.where(dc_officier.columns == '本月提成金额')[0]) + 1):-1]
penalty['员工编号'] = dc_officier['员工编号']



dc_of['仓管员奖金池合计'] =  dc_of['主管(副主管)奖金池合计'] + dc_of['仓管员奖金池合计']
dc_of = dc_of.drop(columns='主管(副主管)奖金池合计')
# dc_of = dc_of.drop(columns='本月网点正 / 副主管KPI得分')

## 核对 奖金池合计
# collist = list(dc_of)[11:int(np.where(dc_officier.columns == '仓管员奖金池合计')[0]) - 1]
# dc_of['仓管员奖金池合计'] = dc_of[collist].apply(np.sum, axis=1)
# *****************************************************************
# 仓管员KPI得分
dc_of = supervisor_kpi.officer_kpi(dc_of,path, flist)
print('01.仓管KPI计算完成')
# # 计算仓管奖金池
# dc_of['应发奖金池'] = dc_of['仓管员奖金池合计'] * dc_of[r'本月网点仓管KPI得分'] * 0.01

## 复称奖励*************************
# [dc_of, check] = reweight_reward.reweight_reward(dc_of, path, flist)
# print('01.复称奖励计算完成')
## buddy*************************
[dc_of, check] = buddy_incentive.buddy_incentive(dc_of, path, flist)
check = check.append(check)
print('02.buddy奖励计算完成')
## FDC*************************
[dc_of, ck] = FDC_incentive.FDC_incentive(dc_of, path, flist)
check = check.append(ck)
print('03.FDC奖励计算完成')
## FDC*************************
[dc_of, ck] = support_incentive.support_courierV2(dc_of, path, flist)
check = check.append(ck)
print('04.支援补贴计算完成')
## 场地补贴*************************
[dc_of, ck] = site_incentive.site_incentive(dc_of, path, flist)
check = check.append(ck)
print('05.场地补贴计算完成')
# ##水果件计算
# [dc_of, ck] = fruit.fruit_reward(dc_of, path, flist)
# check = check.append(ck)
# print('06.水果件计算完成')
## 内推奖励*************************
# [dc_of, ck] = maintenance_reward.recommend_reward(dc_of, path, flist)
# check = check.append(ck)
# print('06.内推奖励计算完成')

## 错分包裹补贴*************************
[dc_of, ck] = support_incentive.misclassified_parcel_amount(dc_of, path, flist)
check = check.append(ck)
print('06.错分包裹补贴计算完成')

## 揽收称重不准确复称奖励************************************
[dc_of, ck] = support_incentive.inaccurate_weigh_reward(dc_of, path, flist)
check = check.append(ck)
print('07.揽收称重不准确复称奖励计算完成')

## CDC月度补贴*************************
[dc_of, ck] = cdc_reward.cdc_reward(dc_of, path, flist)
check = check.append(ck)
print('08.CDC月度补贴计算完成')

## 大件操作补贴*************************仓管
[dc_of, ck] = support_incentive.large_operation_subsidy(dc_of, path, flist)
check = check.append(ck)
print('09.大件操作补贴计算完成')
## 芭提雅&普吉岛补贴*************************
[dc_of, ck] = support_incentive.Pattaya_Phuket_Subsidy(dc_of, path, flist)
check = check.append(ck)
print('10.芭提雅&普吉岛补贴计算完成')



# 7&9&10月上报违规奖励*****************************
# [dc_of, ck] = support_incentive.violation_reward(dc_of, path, flist)
# check = check.append(ck)
# print('08.上报违规奖励计算完成')

# # 仓管员KPI得分
# dc_of = supervisor_kpi.officer_kpi(dc_of,path, flist)
# print('01.仓管KPI计算完成')
# 计算仓管奖金池
dc_of['应发奖金池'] =  dc_of['仓管员奖金池合计'] * dc_of[r'本月网点仓管KPI得分'] * 0.01


# 以下为罚款项目计算-------------------------------------
[penalty, ck] = inef_outsc.inef_outsc(penalty, path, flist)
check = check.append(ck)
print('10.低效外协处罚计算完成')
[penalty, ck] = phone_cost.phone_cost(penalty, path, flist)
check = check.append(ck)
print('11.补扣话费计算完成')
[penalty, ck] = deduction_wage.deduction_wage(penalty, path, flist)
check = check.append(ck)
print('12.补扣工资计算完成')
[penalty, ck] = damage_device.damage_device(penalty, path, flist)
check = check.append(ck)
print('13.平摊维修费用计算完成')
[penalty, ck] = false_scan_penalty.false_scan_penalty(penalty, path, flist)
check = check.append(ck)
print('21.虚假扫描罚款计算完成')

# penalty = keeper_ratio.keeper_ratio(penalty, path, flist)
# print('14.揽件人效系数计算完成')


[penalty, ck] = over_wage.over_wage(penalty, path, flist)
check = check.append(ck)
print('14.多发补扣计算完成')



# 以下进行数据整合-*****************************************
idx = (np.where(dc_of.columns == '仓管员奖金池合计'))[0][0]
# idx = (np.where(dc_of.columns == '本月网点仓管KPI得分')[0])
dc_of['本月提成金额฿'] = dc_of.iloc[:, idx:].apply(np.sum, axis=1)
# dc_of['本月提成金额฿'] = dc_of['本月提成金额฿']
dc_of = pd.merge(dc_of, penalty, how='left', left_on='员工编号', right_on='员工编号')
# 提成数据整合
dc_of = integra.officer_intg(dc_of)
dc_of = dc_of.drop(columns='该员工提成计算规则')
dc_of = dc_of.drop(columns='网点类型')
##保存数据
current_month = pd.ExcelWriter(output + '00.本月提成结果_officier.xlsx')
dc_of.to_excel(current_month, sheet_name='dc_officier', index=False)
current_month.save()
print('98.officer提成计算完成并保存')




# 添加校验结果
# 每日数据校验
check = check.append(
    pd.DataFrame({'原始字段': ['每日提成合计'], '原始数据汇总': [dc_officier['主管(副主管)奖金池合计'].sum() + dc_officier['仓管员奖金池合计'].sum()],
                  '提成数据汇总': [dc_of['仓管员奖金池合计'].sum()]}))
# 罚款数据校验
check = check.append(pd.DataFrame({'原始字段': ['仓管员当月罚款合计'], '原始数据汇总': [dc_officier['个人罚款合计'].sum()],
                                   '提成数据汇总': [penalty['个人罚款合计'].sum()]}))
# 汇总校验
check = check.append(pd.DataFrame({'原始字段': ['汇总校验'], '原始数据汇总': [dc_of['本月提成金额฿'].sum() - dc_of['个人罚款合计'].sum()],
                                   '提成数据汇总': [dc_of['本月应发放提成฿'].sum()]}))
today = str(get_current_date())
checkWriter = pd.ExcelWriter(output + '01.officier校验结果' + str(get_current_date()) + '.xlsx')
check.to_excel(checkWriter, sheet_name='dc_officier', index=False)
checkWriter.save()
print('98.officer校验结果已保存\n')
