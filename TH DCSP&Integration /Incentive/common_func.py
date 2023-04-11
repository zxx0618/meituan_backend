# coding=utf-8
# 发送邮件需要的库
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import make_header
# 数据操作需要的库
import pandas as pd
# 系统库
import os
import sys
from datetime import datetime, date
from datetime import timedelta
from email.header import make_header
# 多线程库
from concurrent.futures import ThreadPoolExecutor
# 数据库操作的库
from sqlalchemy import create_engine
from pymysql.cursors import DictCursor
import pymysql
import time, datetime
# 爬虫库
import requests
import urllib.request as request
# 拷贝所需要的库
import shutil
# 输出日志所需要的库
import logging
from logging import handlers
from functools import wraps
import traceback


#########################################################################
# 发送邮件类

def send_email(options):
    '''
    发送不带附件的邮件函数
    options = {
        'sender': 'wuxiangshen@flashexpress.com',  # 发件人
        'receivers': ['wuxiangshen@flashexpress.com', 'wuxs231@163.com'],  # 收件人，是一个list
        'cc': ['wuxiangshen@flashexpress.com, wuxs231@163.com'],  # 抄送人
        'username': 'wuxiangshen@flashexpress.com',  # 发件人的邮箱用户名
        'password': 'hdU5hE8oVf6CmADP',  # 发件人的邮箱密码
        'from_person': 'wuxiangshen@flashexpress.com',  # 发件人的名字
        'title': 'test',  # 邮件标题
        'host': 'smtp.exmail.qq.com',  # 邮件host服务器
        'content': 'test',  # 邮件的正文内容
    }
    :return:
    '''
    message = MIMEText(options['content'], 'html', 'utf-8')  # 邮件内容
    message['From'] = Header(options['from_person'], 'utf-8')  # 发件人
    message['To'] = Header(','.join(options['receivers']), 'utf-8')  # 收件人
    if len(options['cc']) > 0:
        message['Cc'] = Header(','.join(options['cc']), 'utf-8')  # 抄送人
    subject = options['title']  # 邮件标题
    message['Subject'] = Header(subject, 'utf-8')  # 主题

    try:
        # smtpObj = smtplib.SMTP(options['host'])  # smtp服务器地址
        smtpObj = smtplib.SMTP_SSL(options['host'], port=465)  # qq邮箱使用
        # smtpObj.starttls()  # 解决登录问题
        smtpObj.login(options['username'], options['password'])  # 登录
        smtpObj.sendmail(options['sender'], options['receivers'] + options['cc'], message.as_string())  # 发送邮件
        smtpObj.quit()  # 退出
        print("邮件发送成功")

    except smtplib.SMTPException as e:
        print("Error: 无法发送邮件", e)
        return None


def send_email_with_attach(options):
    '''
    发送带附件的邮件函数
    options = {
        'sender': 'wuxiangshen@flashexpress.com',  # 发件人
        'receivers': ['wuxiangshen@flashexpress.com', 'wuxs231@163.com'],  # 收件人，是一个list
        'cc': ['wuxiangshen@flashexpress.com, wuxs231@163.com'],  # 抄送人
        'username': 'wuxiangshen@flashexpress.com',  # 发件人的邮箱用户名
        'password': 'hdU5hE8oVf6CmADP',  # 发件人的邮箱密码
        'from_person': 'wuxiangshen@flashexpress.com',  # 发件人的名字
        'title': 'test',  # 邮件标题
        'host': 'smtp.exmail.qq.com',  # 邮件host服务器
        'content': 'test',  # 邮件的正文内容
        'xlsx_name': save_dir,   # 要读取的附件excel内容
        'fujian_name': fujian_name  # 附件的名称
    }
    :return:
    '''

    # 创建一个带附件的实例
    message = MIMEMultipart()
    # 邮件基本信息
    message_content = MIMEText(options['content'], 'html', 'utf-8')  # 邮件内容
    message['From'] = Header(options['from_person'], 'utf-8')  # 发件人
    message['To'] = Header(','.join(options['receivers']), 'utf-8')  # 收件人
    if len(options['cc']) > 0:
        message['Cc'] = Header(','.join(options['cc']), 'utf-8')  # 抄送人
    message['Subject'] = Header(options['title'], 'utf-8')  # 主题
    message.attach(message_content)

    # 构造附件1
    # 读取文件
    att1 = MIMEText(open(options['xlsx_name'], 'rb').read(), 'base64', 'UTF-8')
    # 用make_header
    att1["Content-Type"] = 'application/octet-stream;name="%s"' % make_header(
        [(options['fujian_name'], 'UTF-8')]).encode('UTF-8')
    att1["Content-Disposition"] = 'attachment;filename= "%s"' % make_header([(options['fujian_name'], 'UTF-8')]).encode(
        'UTF-8')
    # 把附件加载到邮件中
    message.attach(att1)
    #补丁，添加多附件
    morefile = options['more_file']
    if len(morefile)>0:
        for files in morefile:
            att1 = MIMEText(open(files, 'rb').read(), 'base64', 'UTF-8')
            att1["Content-Type"] = 'application/octet-stream;name="%s"' % make_header([(files.split('/')[-1] ,'UTF-8')]).encode('UTF-8')
            att1["Content-Disposition"] = 'attachment;filename= "%s"' % make_header([(files.split('/')[-1], 'UTF-8')]).encode('UTF-8')
            message.attach(att1)

    try:
        # smtpObj = smtplib.SMTP(options['host'])  # smtp服务器地址
        smtpObj = smtplib.SMTP_SSL(options['host'], port=465)  # qq邮箱使用
        # smtpObj.starttls()  # 解决登录问题
        smtpObj.login(options['username'], options['password'])  # 登录
        smtpObj.sendmail(options['sender'], options['receivers'] + options['cc'], message.as_string())  # 发送邮件
        smtpObj.quit()  # 退出
        print("邮件发送成功")

    except smtplib.SMTPException as e:
        print("Error: 无法发送邮件", e)
        return None


#################################################################################
# 时间日期类

def timestamp_to_strtime(timestamp):
    '''
    时间戳转为字符串格式
    :param timestamp:
    :return:
    '''
    try:
        timestruct = time.localtime(timestamp)
        strtime = time.strftime('%Y-%m-%d %H:%M:%S', timestruct)
        return strtime

    except Exception as e:
        print('时间转换出错：%s' % e)
        return None


def strtime_to_timestamp(strtime):
    '''
    字符串转为时间戳
    :param time_in:
    :return:
    '''
    try:
        # 获取字符串时间
        day_time = str(strtime)
        # 转换成时间元组
        timearray = time.strptime(day_time, "%Y-%m-%d %H:%M:%S")
        # 转换成时间戳
        timestamp = int(time.mktime(timearray))

        return timestamp

    except Exception as e:
        print('时间转换出错：%s' % e)
        return None


def get_current_date(is_chinese=False):
    '''
    获取当前日期
    :param is_chinese:
    :return:‘2019-03-19’
    '''
    import time
    import locale
    if not is_chinese :
        return time.strftime('%Y-%m-%d')
    elif is_chinese:
        locale.setlocale(locale.LC_CTYPE, 'chinese')
        return time.strftime('%Y年%m月%d日')


def get_current_time(is_chinese=False):
    '''
    获取当前时间
    :param is_chinese:
    :return:‘2019-03-19 07:09:07’
    '''
    import time
    import locale
    if not is_chinese :
        return time.strftime('%Y-%m-%d %H:%M:%S')
    elif is_chinese:
        locale.setlocale(locale.LC_CTYPE, 'chinese')
        return time.strftime('%Y年%m月%d日%H时%M分%S秒')


###################################################################################
# 提效类

def multiprocess(func, query_list, workers=10):
    '''
    多线程函数
    :param func: 执行函数
    :param query_list: 参数组成的list
    :param workers: 默认10个线程
    :return:
    '''
    try:
        length = len(query_list)  # 统计list长度，用来安排线程数
        if length < workers:
            if length == 0:
                return print('list为空')
            else:
                n = length
        else:
            n = workers

        # 多线程执行
        with ThreadPoolExecutor(n) as executor:
            executor.map(func, query_list)
        print('done')

    except Exception as e:
        print('error:%s' % e)
        return None


##########################################################################################
# 数据库操作类

def df_to_sql(engine_conn, data, table_name, method='append'):
    '''
    datafrme格式的数据直接写入数据库
    :param engine_conn:数据库连接引擎
    :param data:要存入的字典格式格式的数据
    :param table_name:要存的表名
    :return:
    '''
    try:
        # list形式的字典转为dataframe格式
        df = pd.DataFrame(data)
        # 创建连接数据库的引擎
        engine = create_engine('%s' % engine_conn)
        # 写入数据，如果要替换原来的数据，则用replace
        if method == 'append':
            df.to_sql(name=table_name, con=engine, if_exists='append', index=False, index_label=False)
        elif method == 'replace':
            df.to_sql(name=table_name, con=engine, if_exists='replace', index=False, index_label=False)
        else:
            return '参数错误'
        # 关闭engine的连接

        engine.dispose()
        # print('写入数据库成功')
    except Exception as e:
        print('dataframe存入数据库失败：%s' % e)
        return None


def list_to_df_to_sql(tb_name, cols, rows, engine_conn):
    '''
    list转dict转df
    :param tb_name:表名
    :param cols:列字段
    :param rows:行数据，仅限一行
    :param engine_conn:数据库连接引擎
    :return:
    '''
    try:
        # 先把列和行转成字典
        dict_temp = dict(zip(cols, rows))
        # 再把字典转换成list
        list_temp = [dict_temp]
        # 最后转为dataframe
        df = pd.DataFrame(list_temp)
        # 构造连接数据库的引擎
        engine = create_engine('%s' % engine_conn)
        # df写入数据库
        df.to_sql(name=tb_name, con=engine, if_exists='append', index=False, index_label=False)
        # 关闭连接引擎
        engine.dispose()
        print('写入数据库成功')

    except Exception as e:
        print('list存入数据库失败：%s' % e)
        return None


def sql_to_df(engine_info, sql):
    '''
    数据库读取为dataframe格式
    :param engine_info:数据库连接引擎
    :param sql:操作的sql语句
    :return: 输出字典格式的数据
    '''
    try:
        # 创建数据库连接引擎
        engine = create_engine(engine_info)
        # 从数据库读取结果为dataframe
        df_query = pd.read_sql(sql, engine)
        # 关闭数据库连接
        engine.dispose()
        print('数据库读取完毕', df_query.head())
        # 转为字典list
        data = df_query.to_dict(orient='dict')
        return data

    except Exception as e:
        print('从数据库读取为df失败:%s' % e)
        return None


def sql_save_as_file(canshu):
    '''
    sql查询的字典数据保存为excel文件的函数
    :param canshu:这是一个字典，格式：
    canshu = {
        'save_path': 保存路径,
        'down_path': 下载路径,
        'filename': 保存的文件名,
        'data': 字典格式的数据库查询结果
    }
    :return:
    '''
    try:
        save_path = canshu['save_path']
        # down_path = canshu['down_path']
        filename = canshu['filename']

        save_dir = os.path.join(save_path, filename)  # 生成存储路径
        # url = os.path.join(down_path, filename)  # 生成下载路径

        df = pd.DataFrame(canshu['data'])  # 字典格式的data转换为dataframe格式

        if 'suoyin' in df.columns:  # 按索引排序
            df = df.sort_values(by='suoyin', axis=0, ascending=True)
            del df['suoyin']
        if 'id' in df.columns:  # 删除id列
            del df['id']

        print('df', df.head())

        # 保存文件
        writer = pd.ExcelWriter(save_dir)
        df.to_excel(writer, '%s' % filename, index=False)
        writer.save()

        return save_dir

    except Exception as e:
        print('保存为文件出错', e)
        return None


def sql_read_dict(sql, conn):
    '''
    使用sql语句从数据库中一次性读取
    :param sql:操作的说sql语句
    :param conn:数据库连接的字典
    :return: 返回字典型结果
    '''
    try:
        # 连接数据库
        conn = pymysql.connect(**conn)
        cur = conn.cursor(DictCursor)
        # 提交sql语句
        cur.execute(sql)
        # 获取查询结果
        results = cur.fetchall()
        # 提交事务执行
        conn.commit()
        # 关闭连接
        cur.close()
        conn.close()

        return results

    except Exception as e:
        print('数据库操作失败：%s' % e)
        return None


def sql_caozuo(sql, conn):
    '''
    使用sql语句从数据库中一次性读取
    :param sql:操作的说sql语句
    :param conn:数据库连接的字典
    :return: 返回元组型结果
    '''
    try:
        # 连接数据库
        conn = pymysql.connect(**conn)
        cur = conn.cursor()
        # 提交sql语句
        cur.execute(sql)
        # 获取查询结果
        results = cur.fetchall()
        # 提交事务执行
        conn.commit()
        # 关闭连接
        cur.close()
        conn.close()

        return results

    except Exception as e:
        print('数据库操作失败：%s' % e)
        return None


########################################################################################
# 文件操作类

def clear_dir(filename, path):
    '''
    删除文件
    :param filename: 文件名
    :param path: 文件所在的上层路径
    :return:
    '''
    try:
        ls = os.listdir(path)
        for i in ls:
            if i == filename:
                filepath = os.path.join(path, filename)
                os.remove(filepath)
                print('删除成功', filename)

    except Exception as e:
        print('删除文件失败：%s' % e)
        return None


def delete_file(file_dir, del_file, type='file', bianli=0):
    '''
    删除文件
    :param file_dir: 搜索路径
    :param del_file: 要删除的文件
    :param type: 文件为'file', 目录为'dir'
    :param bianli: 是否遍历，默认0不遍历，1遍历循环删除
    :return:
    '''
    try:
        a = 0
        for item in os.listdir(file_dir):
            filename = str(file_dir) + "/" + str(item)
            if type == 'dir':
                if os.path.isdir(filename):
                    if str(item) == str(del_file):
                        os.removedirs(filename)
                        a += 1
                else:
                    if bianli == 1:
                        # 遍历寻找文件夹并删除
                        delete_file(filename, del_file, type='dir', bianli=1)

            elif type == 'file':
                if os.path.isfile(filename):
                    if str(item) == str(del_file):
                        os.remove(filename)
                        a += 1

                elif os.path.isdir(filename):
                    if bianli == 1:
                        # 遍历删除
                        delete_file(filename, del_file, type='file', bianli=1)

        if a == 0:
            print('目标没找到')
            return '0'
        else:
            print('删除%s个目标' % a)
            return '1'

    except Exception as e:
        print('delete file error: %s' % e)
        return None


def copy_func(fromdir, todir, type='file'):
    '''
    拷贝目录或者文件
    :param fromdir: 源路径
    :param todir: 目标路径
    :param type: 文件or目录，默认是文件
    :return:
    '''
    if type == 'file':
        shutil.copyfile(fromdir, todir)
        print('文件复制成功')
    elif type == 'dir1':
        shutil.copytree(fromdir, todir)
        print('目录复制成功')


def unzip_tar_gz_file(fname):
    '''
    tar和gz后缀的文件解压
    :param fname:
    :return:
    '''
    try:
        if fname.endswith("tar.gz"):
            tar = tarfile.open(fname, "r:gz")
            tar.extractall()
            tar.close()

        elif fname.endswith("tar"):
            tar = tarfile.open(fname, "r:")
            tar.extractall()
            tar.close()
        else:
            print('文件后缀不正确')
    except Exception as e:
        print('unzip_tar_gz_file error: %s' % e)
        return None


###################################################################################
# 日志输出

class Logger(object):
    level_relations = {
        'debug':logging.DEBUG,
        'info':logging.INFO,
        'warning':logging.WARNING,
        'error':logging.ERROR,
        'crit':logging.CRITICAL
    }  # 日志级别关系映射

    def __init__(self, filename, level='info', when='D',backCount=3,
                 fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'):
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)  # 设置日志格式
        self.logger.setLevel(self.level_relations.get(level))#设置日志级别
        sh = logging.StreamHandler()  # 往屏幕上输出
        sh.setFormatter(format_str)  # 设置屏幕上显示的格式
        # 往文件里写入指定间隔时间自动生成文件的处理器
        th = handlers.TimedRotatingFileHandler(filename=filename,
                                               when=when,
                                               backupCount=backCount,
                                               encoding='utf-8')
        # 实例化TimedRotatingFileHandler
        # interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒、 M 分、 H 小时、 D 天、 W 每星期（interval==0时代表星期一）、 midnight 每天凌晨
        th.setFormatter(format_str)  # 设置文件里写入的格式
        self.logger.addHandler(sh)  # 把对象加到logger里
        self.logger.addHandler(th)


# 首先定义一个log函数
def get_logger():
    # 获取logger实例，如果参数为空则返回root logger
    logger = logging.getLogger('test')
    if not logger.handlers:
        # 指定logger输出的格式
        formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')

        # 文件日志
        file_handler = logging.FileHandler(log_path, encoding='utf8')
        # 可以通过setFormatter指定输出格式
        file_handler.setFormatter(formatter)

        # 控制台日志
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.formatter = formatter  # 也可以直接给formatter赋值

        # 为logger添加的日志处理器
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        # 指定日志的输出级别，默认为warn级别
        logger.setLevel(logging.INFO)

    # 添加下面一句，在记录日志之后移除句柄
    return logger


# 然后定义一个装饰器函数，目的为了保持引用进来的函数名字不会发生变化
def decoratore(func):
    @wraps(func)
    def log(*args, **kwargs):
        try:
            print("当前运行方法：", func.__name__)
            return func(*args, **kwargs)
        except Exception as e:
            print('decoatore error:%s' % e)
            get_logger().error(f"{func.__name__} is error, here are details:{traceback.format_exc()}")
    return log




