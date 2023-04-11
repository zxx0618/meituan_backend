# coding=utf-8

from common_func import *
from common_config import *
from raw_dir import *
from addin.remove_duplicate import *

# 生成DSCP待确认的文件格式***********************

## 设置工作路径

os.chdir(output)
today = str(get_current_date())
# 找到成的文件================================================

flist = os.listdir()
for ex in flist:
    if ex.find('提成结果_boatcourier') > -1:
        bc = pd.read_excel(ex)
        print('boat_courier读取完毕')
    if ex.find('提成结果_courier') > -1:
        cr = pd.read_excel(ex)
        print('courier读取完毕')
    if ex.find('提成结果_officier') > -1:
        of = pd.read_excel(ex)
        print('DCofficier读取完毕')
    if ex.find('提成结果_supervisor') > -1:
        sup = pd.read_excel(ex)
        print('DCsupervisor读取完毕')
print('===>提成文件读取完毕')

# 对快递员和仓管去重
crid = cr[['员工编号']]
crid.insert(1, '提成类型', 'DC快递员提成')
# crid['提成类型']='快递员提成'
ofid = of[['员工编号']]
ofid.insert(1, '提成类型', 'DC仓管员提成')
supid = sup[['员工编号']]
supid.insert(1, '提成类型', 'DC主管提成')
cr_of = pd.merge(crid, ofid, left_on='员工编号', right_on='员工编号', how='inner')
# 重复数据为：增值服务提成、复称奖励、buddy奖励、FDC、支援补贴、找场地奖励、疫情补贴、扣话费、补扣工资；
cr = rm_dcsp_dup(cr, cr_of)

# 对快递员和主管去重
cr_sup = pd.merge(crid, supid, left_on='员工编号', right_on='员工编号', how='inner')
# 重复数据为：增值服务提成、复称奖励、buddy奖励、FDC、支援补贴、找场地奖励、疫情补贴、扣话费、补扣工资；
cr = rm_dcsp_dup(cr, cr_sup)

# 对仓管和主管去重
sup_of = pd.merge(supid, ofid, left_on='员工编号', right_on='员工编号', how='inner')
of = rm_dcsp_dup(of, sup_of)
print(sup_of)

repeat = cr_of
repeat = repeat.append(cr_sup)
repeat = repeat.append(sup_of)
repeat.to_excel('repeat_1.xlsx')
print('===>去重完毕')

## 保存整合后的去重数据，保存为待确认版
# 快递员揽派件提成
SQL1 = """
SELECT fd.`stat_date` 日期,
       fd.`store_id` 网点ID,
       ss.`name` 网点名称,
       CASE fd.`category` when 1 then '揽件' when 2 THEN '派件' end as 揽派件,
       SUM(fd.`quantity`) 单量,
       SUM(fd.`amount`) 提成金额
  FROM `bi_pro`.`finance_courier_achievements_v3` fd
  LEFT JOIN `fle_staging`.`sys_store` ss on fd.`store_id`= ss.`id`
 where fd.`stat_date` >=  CURRENT_DATE - INTERVAL day(CURRENT_DATE) -1 day -INTERVAL 1 month
   and fd.`stat_date` < CURRENT_DATE - INTERVAL day(CURRENT_DATE) -1 day
   and fd.`type`= 1
 GROUP BY fd.`stat_date`,
         fd.`store_id`,
         fd.`category`
"""
# 主管揽派件提成
SQL2 = """
select fk.staff_info_id,
       fk.store_id,
       ss.name,
       case fk.type when 3 THEN '主管' when 7 then '副主管' END as 职位,
       fk.admin_this_average*(30-0.5*4) NW揽件量,
        -- 每月天数-0.5*法定假日天数
       sum(admin_notnw_pickup_orig) 非NW揽件量,
       sum((fk.`admin_amount_pickup`+ fk.`admin_notnw_pickup_count` *0.3) *admin_percent/100) 揽件提成,
       sum(fk.delivery_count) 派件量,
       sum(fk.delivery_count*0.3*admin_percent/100) 派件提成
  from `bi_pro`.`finance_keeper_manager_month` fk
  left join `fle_staging`.`sys_store` ss on ss.id= fk.store_id
  left join `fle_staging`.`staff_info` si on si.id= fk.`staff_info_id`
  where fk.`stat_date` >=  CURRENT_DATE - INTERVAL day(CURRENT_DATE) -1 day -INTERVAL 1 month
   and fk.`stat_date` < CURRENT_DATE - INTERVAL day(CURRENT_DATE) -1 day
   and fk.type in (3, 7) 
 group by fk.staff_info_id
"""
# 添加大区片区
SQL3 = """
select fk.store_id,
       smp.`name` as 片区名称,
       smr.name as 大区名称
  from `bi_pro`.`finance_keeper_manager_month` fk
  left join `fle_staging`.`sys_store` ss on ss.id= fk.store_id
  LEFT JOIN `sys_manage_piece` smp on ss.`manage_piece`= smp.`id`
  LEFT JOIN `sys_manage_region` smr on ss.`manage_region`= smr.`id`
 where fk.stat_date>= CURRENT_DATE - INTERVAL day(CURRENT_DATE) -1 day-INTERVAL 1 month
   and fk.stat_date< CURRENT_DATE - INTERVAL day(CURRENT_DATE) -1 day
"""
SQL4 = """
select fk.store_id,
       ss.name,
       smp.`name` as 片区名称,
       smr.name as 大区名称,
       sum(if(fk.`type`= 2, fk.pool, 0)) 仓管奖金池,
       sum(if(fk.`type`!= 2, fk.pool, 0)) 主管奖金池,
       sum(fk.pool) 总奖金池
  from `bi_pro`.`finance_keeper_manager_month` fk
  left join `fle_staging`.`sys_store` ss on ss.id= fk.store_id
  LEFT JOIN `sys_manage_piece` smp on ss.`manage_piece`= smp.`id`
  LEFT JOIN `sys_manage_region` smr on ss.`manage_region`= smr.`id`
 where fk.stat_date>= CURRENT_DATE - INTERVAL day(CURRENT_DATE) -1 day-INTERVAL 1 month
   and fk.stat_date< CURRENT_DATE - INTERVAL day(CURRENT_DATE) -1 day
 group by 1
 ORDER BY 1
"""

SQL5 = """
select am.store_id as 网点,
       ss.`name` as 网点名称,
       smp.`name` as 片区名称,
       smr.name as 大区名称,
       sum(if(am.`abnormal_object`=0,am.`punish_money` ,0)) 个人罚款合计,
       sum(if(am.`abnormal_object`=1,am.`punish_money` ,0)) 集体罚款合计,
       sum(am.punish_money) as 罚款合计
  from bi_pro.abnormal_message am
  LEFT JOIN `fle_staging`.`sys_store` ss on am.`store_id`= ss.`id`
  LEFT JOIN `fle_staging`.`sys_manage_piece` smp on ss.`manage_piece`= smp.`id`
  LEFT JOIN `fle_staging`.`sys_manage_region` smr on ss.`manage_region`= smr.`id`
 where am.abnormal_time>= CURRENT_DATE - INTERVAL day(CURRENT_DATE )-1 day -INTERVAL 1 month
   and am.abnormal_time< CURRENT_DATE - INTERVAL day(CURRENT_DATE )-1 day
   and am.state= 1
   and am.`isdel`= 0
   and ss.`category` in(1,2, 10)
 group by am.store_id
"""

engine_ads = create_engine(engine_info_ads)
courier = pd.read_sql(SQL1, engine_ads)
keeper = pd.read_sql(SQL2, engine_ads)
region = pd.read_sql(SQL3, engine_ads)
engine_ads.dispose()

Writer = pd.ExcelWriter(output + 'TH_DCSP_绩效_待确认_' + today + '.xlsx')
bc.to_excel(Writer, sheet_name='DC_boatcourier', index=False)
cr.to_excel(Writer, sheet_name='DC_courier', index=False)
of.to_excel(Writer, sheet_name='DC_officier', index=False)
sup.to_excel(Writer, sheet_name='DC_supervisor', index=False)
# courier.to_excel(Writer, sheet_name='快递员揽派件提成', index=False)
# keeper.to_excel(Writer, sheet_name='主管揽派件提成', index=False)
Writer.save()
Writer.close()
print('提成计算-=去重=-待确认并保存')

##筛选出提成较低的快递员和仓管员
of_low = of[of[u'本月应发放提成฿'] < 500]
sup_low = sup[sup[u'本月应发放提成฿'] < 1000]

Wt = pd.ExcelWriter(output + 'TH_DCSP_绩效_低提成_' + today + '.xlsx')
of_low.to_excel(Wt, sheet_name='仓管提成小于500泰铢', index=False)
sup_low.to_excel(Wt, sheet_name='主管提成1000泰铢', index=False)
Wt.save()
Wt.close()
print('提成计算-=鼓励名单=-待确认并保存')

##筛选出消极怠工的仓管员
of_slack = of[['网点', '网点名称', '员工编号', '员工名称', '在职状态', '员工类型', '职位', '入职日期', '个人罚款合计', r'本月应发放提成฿']]
of_slack.insert(10, '平均罚款', of_slack['个人罚款合计'].mean())
of_slack.insert(11, '平均应发放提成', of_slack[r'本月应发放提成฿'].mean())
of_slack = of_slack[(of_slack['个人罚款合计'] > of_slack['平均罚款']) &
                    (of_slack[r'本月应发放提成฿'] < of_slack['平均应发放提成']) &
                    (of_slack['在职状态'] == '在职')]

of_slack = pd.merge(of_slack, region, left_on='网点', right_on='store_id', how='left')
of_slack.drop(columns='store_id')
Wt = pd.ExcelWriter(output + 'TH_DCSP_消极怠工仓管员_' + today + '.xlsx')
of_slack.to_excel(Wt, sheet_name='消极怠工仓管员', index=False)
Wt.save()
Wt.close()
print('提成计算-=鼓励名单=-待确认并保存')
