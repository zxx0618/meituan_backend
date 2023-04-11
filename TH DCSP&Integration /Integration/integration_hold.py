# coding=utf-8
import dict
from common_func import *
from addin.hold_remove import *
from raw_dir import *

# 以下为自定义函数

## 设置工作路径
os.chdir(output)

# 找到成的文件================================================
flist = os.listdir()
for ex in flist:
    if ex.find(r'TH_DCSP&HUB&Onsite_绩效_已确认') > -1:
        bc = pd.read_excel(ex, sheet_name='DC_boatcourier')
        cr = pd.read_excel(ex, sheet_name='DC_courier')
        print('DCcourier读取完毕')
        of = pd.read_excel(ex, sheet_name='DC_officier')
        sup = pd.read_excel(ex, sheet_name='DC_supervisor')
        print('DCsupervisor读取完毕')
        mp = pd.read_excel(ex, sheet_name='DC_大区片区')
        hstf = pd.read_excel(ex, sheet_name='HUB_仓管员')
        print('HUB_仓管员读取完毕')
        hman = pd.read_excel(ex, sheet_name='HUB_主管')
        print('HUB_主管读取完毕')
        ont = pd.read_excel(ex, sheet_name='OnSite')
        print('Onsite提成读取完毕')
    if ex.find(r'hold') > -1:
        hold = pd.read_excel(ex)
        print('HOLD提成读取完毕')
        hold = hold.rename(columns={u"Employee No.": 'hold'})
        hold = hold[['hold']]

# 表头需要先手动调整，员工编号放在第三列

# 其它的数据整理，主管和仓管的表头调整；
# of=of.drop(columns = [r'本月应发放提成฿',r'低提成补贴'])
# of=of.rename(columns={u"最终发放":u'本月应发放提成฿'})
# sup=sup.drop(columns = [r'本月应发放提成฿',r'低提成补贴'])
# sup=sup.rename(columns={u"最终发放":u'本月应发放提成฿'})
ont = ont.drop(columns=[r'离职日期', r'停职日期', '出差天数'])

# 添加$
bc['本月提成金额฿'] = round(bc['本月提成金额฿'], 2).astype(str) + '฿'
cr['快递员当月应发放提成金额฿'] = round(cr['快递员当月应发放提成金额฿'], 2).astype(str) + '฿'
of['本月应发放提成฿'] = round(of['本月应发放提成฿'], 2).astype(str) + '฿'
sup['本月应发放提成฿'] = round(sup['本月应发放提成฿'], 2).astype(str) + '฿'
mp['本月提成金额฿'] = round(mp['本月提成金额฿'], 2).astype(str) + '฿'
hstf['当月应发金额总计'] = round(hstf['当月应发金额总计'], 2).astype(str) + '฿'
hman['当月应发金额总计'] = round(hman['当月应发金额总计'], 2).astype(str) + '฿'
ont['实发提成'] = round(ont['实发提成'], 2).astype(str) + '฿'

# 提成系数中要加“Raking”
mp['提成系数Raking'] = mp['提成系数Raking'].astype(str) + 'Raking'

# HOLD及法院去除
bc = rm_hold(bc, hold)
cr = rm_hold(cr, hold)
of = rm_hold(of, hold)
sup = rm_hold(sup, hold)
mp = rm_hold(mp, hold)
hstf = rm_hold(hstf, hold)
hman = rm_hold(hman, hold)
ont = rm_hold(ont, hold)
print('HOLD剔除完毕')

##删除无用的列,保证第三列为员工编号
# bc=bc.drop(columns = '网点类型')
# cr=cr.drop(columns = '网点类型')
# of=of.drop(columns = '网点类型')
# sup=sup.drop(columns = '网点类型')
# bc=bc.drop(columns = '该员工提成计算规则')
# cr=cr.drop(columns = '该员工提成计算规则')
# of=of.drop(columns = '该员工提成计算规则')
# sup=sup.drop(columns = '该员工提成计算规则')

## 表头进行替换
bc = bc.rename(columns=dict.dict)
cr = cr.rename(columns=dict.dict)
of = of.rename(columns=dict.dict)
sup = sup.rename(columns=dict.dict)
mp = mp.rename(columns=dict.dict)
hstf = hstf.rename(columns=dict.dict)
hman = hman.rename(columns=dict.dict)
ont = ont.rename(columns=dict.dict)

print('===>表头翻译完毕')

today = str(get_current_date())
Writer = pd.ExcelWriter(output + '提成结果_翻译上传_' + today + '.xlsx')
bc.to_excel(Writer, sheet_name='DC_boatcourier', index=False)
cr.to_excel(Writer, sheet_name='DC_courier', index=False)
of.to_excel(Writer, sheet_name='DC_officier', index=False)
sup.to_excel(Writer, sheet_name='DC_supervisor', index=False)
mp.to_excel(Writer, sheet_name='DC_大区片区', index=False)
hstf.to_excel(Writer, sheet_name='HUB_仓管员', index=False)
hman.to_excel(Writer, sheet_name='HUB_主管', index=False)
ont.to_excel(Writer, sheet_name='OnSite', index=False)
Writer.save()
Writer.close()
print('提成计算-=翻译=-整合并保存')
