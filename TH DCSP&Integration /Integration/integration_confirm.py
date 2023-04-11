# coding=utf-8

from common_func import *
from raw_dir import *
# from addin.remove_duplicate import *
import addin.low_subsidy as low_subsidy

# 以下为自定义函数

## 设置工作路径,提成文件所在的路径,以及输出路径
os.chdir(output)

# 找到成的文件================================================
flist = os.listdir()
for ex in flist:
    if ex.find('TH_DCSP_') > -1 and ex.find('已确认') > -1:
        bc = pd.read_excel(ex, sheet_name='DC_boatcourier')
        print('DCSP boat 读取完毕')
        cr = pd.read_excel(ex, sheet_name='DC_courier')
        print('DCSP courier 读取完毕')
        of = pd.read_excel(ex, sheet_name='DC_officier')
        print('DCSP officier 读取完毕')
        sup = pd.read_excel(ex, sheet_name='DC_supervisor')
        mp = pd.read_excel(ex, sheet_name='DC_大区片区')
        print('DCSP提成读取完毕')
        print('boat_courier读取完毕')
    # if ex.find('TH_HUB_') > -1 and ex.find('已确认') > -1:
    #     hstf = pd.read_excel(ex, sheet_name='hub_staff')
    #     hman = pd.read_excel(ex, sheet_name='hub_manager')
    #     print('HUB提成读取完毕')
    # if ex.find('TH_Onsite_') > -1 and ex.find('已确认') > -1:
    #     ont = pd.read_excel(ex)
    #     print('OnSite提成读取完毕')
print('===>提成文件读取完毕')

# ＤＣＳＰ 已去重，不用管
# crid = cr[['员工编号']]
# crid.insert(1, '提成类型', 'DC快递员提成')
# ofid = of[['员工编号']]
# ofid.insert(1, '提成类型', 'DC仓管员提成')
# supid = sup[['员工编号']]
# supid.insert(1, '提成类型', 'DC主管提成')
#
# hstfid = hstf[['员工编号']]
# hstfid.insert(1, '提成类型', 'HUB仓管提成')
# hmanid = hman[['员工编号']]
# hmanid.insert(1, '提成类型', 'HUB主管提成')
# ontid = ont[['员工编号']]
# ontid.insert(1, '提成类型', 'Onsite提成')

# # 对DC快递员和HUB仓管去重
# cr_stf = pd.merge(crid, hstfid, left_on='员工编号', right_on='员工编号', how='inner')
# cr = rm_hub_dup(cr, cr_stf)
#
# # 对DC仓管和HUB仓管去重
# of_stf = pd.merge(ofid, hstfid, left_on='员工编号', right_on='员工编号', how='inner')
# of = rm_hub_dup(of, of_stf)
#
# # 对DC仓管和HUB主管去重
# of_hman = pd.merge(ofid, hmanid, left_on='员工编号', right_on='员工编号', how='inner')
# of = rm_hub_dup(of, of_hman)
#
# # 对DC主管和HUB仓管去重
# sup_stf = pd.merge(supid, hstfid, left_on='员工编号', right_on='员工编号', how='inner')
# sup = rm_sup_dup(sup, sup_stf)
#
# # 对DC主管和HUB主管去重
# sup_man = pd.merge(supid, hmanid, left_on='员工编号', right_on='员工编号', how='inner')
# sup = rm_sup_dup(sup, sup_man)
#
# # onsite去重和hub仓管
# ont_stf = pd.merge(ontid, hstfid, left_on='员工编号', right_on='员工编号', how='inner')
# ont = rm_onsite_dup(ont, ont_stf)
#
# repeat = cr_stf
# repeat = repeat.append(of_stf)
# repeat = repeat.append(of_hman)
# repeat = repeat.append(sup_stf)
# repeat = repeat.append(sup_man)
# repeat = repeat.append(ont_stf)
# repeat.to_excel('repeat_2.xlsx')
# print('===>去重完毕')

# 添加上低提成补贴
[of, sup] = low_subsidy.low_subsidy(of, sup, path, flist)

## 保存整合后的去重数据，保存为确定版
today = str(get_current_date())
Writer = pd.ExcelWriter(output + 'TH_DCSP&HUB&Onsite_绩效_已确认_' + today + '.xlsx')
bc.to_excel(Writer, sheet_name='DC_boatcourier', index=False)
cr.to_excel(Writer, sheet_name='DC_courier', index=False)
of.to_excel(Writer, sheet_name='DC_officier', index=False)
sup.to_excel(Writer, sheet_name='DC_supervisor', index=False)
mp.to_excel(Writer, sheet_name='DC_大区片区', index=False)
# hstf.to_excel(Writer, sheet_name='HUB_仓管员', index=False)
# hman.to_excel(Writer, sheet_name='HUB_主管', index=False)
# ont.to_excel(Writer, sheet_name='OnSite', index=False)
Writer.save()
Writer.close()
print('提成计算-=已确定已去重=-保存')
