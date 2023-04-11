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
import addin.supervisor_kpi as supervisor_kpi
import addin.maintenance_reward as maintenance_reward
import addin.add_integration as integra
import addin.over_rage as over_wage
import addin.fruit_reward as fruit
import addin.damage_device as damage_device
import addin.false_scan_penalty as false_scan_penalty

def max_zero(d):
    if d < 0:
        return 0
    else:
        return d


## 设置工作路径
if os.path.isdir(output) == False:
    os.makedirs(output)
os.chdir(path)

## 导入数据
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
supervisor = pd.read_excel(dexcel)
# supervisor=supervisor[supervisor['该员工提成计算规则']!=r'仓管员提成计算规则 = ( 月揽件数*0.7B + 月派件数*0.3B ) / 仓管人数 - 罚款金额']
supervisor = supervisor[supervisor['该员工提成计算规则'].str.contains('主管提成规则') == True]

sup = supervisor.drop(columns=supervisor.columns[int(np.where(supervisor.columns == '本月提成金额')[0]):])

penalty = supervisor.iloc[:, (int(np.where(supervisor.columns == '本月提成金额')[0]) + 1):-1]
penalty['员工编号'] = supervisor['员工编号']
clist = ['虚假问题件 / 虚假留仓件罚款',
         '揽件时称量包裹不准确罚款',
         '包裹丢失罚款',
         '包裹破损罚款',
         'PRI件/SPEED件未妥投包裹罚款',
         '工单处理不及时罚款',
         '5天内未妥投/未中转，且超过一天未更新包裹罚款',
         '5天外未妥投/未中转，且超过一天未更新包裹罚款',
         'minics对问题件解决不及时罚款',
         'miniCS对工单处理不及时罚款',
         '揽收或中转包裹未及时发出包裹罚款',
         '仓管未及时处理问题件包裹罚款',
         '仓管未及时交接speed/优先包裹罚款'
         ]
penalty = penalty.drop(columns=clist)

## KPI*************************
# sup[r'本月网点正 / 副主管KPI得分'] = supervisor_kpi.supervisor_kpi(sup,path,flist)
sup = supervisor_kpi.supervisor_kpi(sup, path, flist)
print('01.主管KPI计算完成')
## 复称奖励*************************
[sup, check] = reweight_reward.reweight_reward(sup, path, flist)
print('02.复称奖励计算完成')
## buddy*************************
[sup, ck] = buddy_incentive.buddy_incentive(sup, path, flist)
check = check.append(ck)
print('03.buddy奖励计算完成')
## FDC*************************
[sup, ck] = FDC_incentive.FDC_incentive(sup, path, flist)
check = check.append(ck)
print('04.FDC奖励计算完成')
## FDC*************************
[sup, ck] = support_incentive.support_courierV2(sup, path, flist)
check = check.append(ck)
print('05.支援补贴计算完成')
## 场地补贴*************************
[sup, ck] = site_incentive.site_incentive(sup, path, flist)
check = check.append(ck)
print('06.场地补贴计算完成')
## 拉新奖励*************************
[sup, ck] = maintenance_reward.maintenance_reward(sup, path, flist)
check = check.append(ck)
print('07.拉新奖励计算完成')
## 内推奖励*************************
[sup, ck] = maintenance_reward.recommend_reward(sup, path, flist)
check = check.append(ck)
print('08.内推奖励计算完成')
## 芭提雅&普吉岛补贴*************************
[sup, ck] = support_incentive.Pattaya_Phuket_Subsidy(sup, path, flist)
check = check.append(ck)
print('9.芭提雅&普吉岛补贴计算完成')

## 内推奖励*************************
# [sup, ck] = support_incentive.violation_reward(sup, path, flist)
# check = check.append(ck)
# print('09.上报违规奖励计算完成')


# ## 拉新奖励*************************
# [sup, ck] = fruit.fruit_reward(sup, path, flist)
# check = check.append(ck)
# print('08.水果件计算完成')
# sup['本月网点正 / 副主管KPI得分'] = sup[['本月网点正 / 副主管KPI得分']].apply(max_zero, axis=1)
# sup['本月网点正 / 副主管KPI得分'] = max_zero(sup['本月网点正 / 副主管KPI得分'])
sup['应发奖金池金额'] = sup['仓管员奖金池合计'] + sup['本月网点正 / 副主管KPI得分'] * sup[r'主管(副主管)奖金池合计'] * 0.01

# 以下为罚款项目计算-------------------------------------
# [penalty, ck] = false_scan_penalty.false_scan_penalty(penalty, path, flist)
# check = check.append(ck)
# print('21.虚假扫描罚款计算完成')
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
# [penalty, ck] = over_wage.over_wage(penalty, path, flist)
# check = check.append(ck)
# print('44.多发补扣计算完成')


# 以下进行数据整合-*****************************************
idx = int(np.where(sup.columns == r'本月网点正 / 副主管KPI得分')[0])
sup['本月提成金额฿'] = sup.iloc[:, (idx + 1):].apply(np.sum, axis=1)
sup = pd.merge(sup, penalty, how='left', left_on='员工编号', right_on='员工编号')
# 提成数据整合
sup = integra.supervisor_intg(sup)
sup = sup.drop(columns='该员工提成计算规则')
sup = sup.drop(columns='网点类型')

current_month = pd.ExcelWriter(output + '00.本月提成结果_supervisor.xlsx')
sup.to_excel(current_month, sheet_name='dc_supervisor', index=False)
current_month.save()
print('98.supervisor提成计算完成并保存')
# 添加校验结果
# 每日数据校验
check = check.append(
    pd.DataFrame({'原始字段': ['每日提成合计'], '原始数据汇总': [supervisor['主管(副主管)奖金池合计'].sum() + supervisor['仓管员奖金池合计'].sum()],
                  '提成数据汇总': [sup['仓管员奖金池合计'].sum()]}))
# 罚款数据校验
check = check.append(pd.DataFrame({'原始字段': ['个人罚款合计'], '原始数据汇总': [supervisor['个人罚款合计'].sum()],
                                   '提成数据汇总': [penalty['个人罚款合计'].sum()]}))
# 汇总校验
check = check.append(pd.DataFrame({'原始字段': ['汇总校验'], '原始数据汇总': [sup['本月提成金额฿'].sum() - sup['个人扣款合计'].sum()],
                                   '提成数据汇总': [sup['本月应发放提成฿'].sum()]}))
today = str(get_current_date())
checkWriter = pd.ExcelWriter(output + '01.supervisor校验结果' + str(get_current_date()) + '.xlsx')
check.to_excel(checkWriter, sheet_name='dc_supervisor', index=False)
checkWriter.save()
print('99.supervisor校验结果已保存\n')
