from collections import Counter

from sqlalchemy import func

from spider.creat_lagou_table import Lagoutables
from spider.creat_lagou_table import Session
import time


class HandleLagouData(object):
    def __init__(self):
        #实例化session信息
        self.mysql_session = Session()
        self.date = time.strftime("%Y-%m-%d",time.localtime())

    #数据的存储方法
    def insert_item(self,item):
        date = time.strftime("%Y-%m-%d",time.localtime()) #抓取时间
        #存储的数据结构
        data = Lagoutables(
            positionId = item['positionId'],  #岗位ID
            positionName=item['positionName'],  # 岗位名称
            companyFullName=item['companyFullName'],  # 公司全称
            companyShortName=item['companyShortName'],  # 公司简称
            companySize=item['companySize'],  # 公司规模
            financeStage=item['financeStage'],  # 公司类型
            city=item['city'],  # 所在城市
            workYear=item['workYear'],  # 工作年限
            education=item['education'],  # 学历
            latitude=item['latitude'],  # 纬度
            longitude=item['longitude'], # 经度
            jobNature=item['jobNature'],    # 岗位性质
            industryField=item['industryField'],  # 业务方向
            positionAdvantage=item['positionAdvantage'],   # 岗位标签
            district=item['district'],   # 公司所在区
            companyLabelList=','.join(item['companyLabelList']),  # 公司福利标签
            salary=item['salary'],#薪资
            crawl_date=date # 抓取日期


        )


        #在存储数据之前，先来查询一下表里是否有这条岗位信息
        query_result = self.mysql_session.query(Lagoutables).filter(Lagoutables.crawl_date==date,
                                                                    Lagoutables.positionId==item['positionId']).first()
        if query_result:
            print('该岗位信息已存在%s:%s:%s'%(item['positionId'],item['city'],item['positionName']))
        else:
            #插入数据
            self.mysql_session.add(data)
            #提交数据到数据库
            self.mysql_session.commit()
            print('新增岗位信息%s'%item['positionId'])

    #行业信息
    def query_industryfield_result(self):
        info = {}
        # 查询今日抓取到的行业信息数据
        result = self.mysql_session.query(Lagoutables.industryField).all()#查询表中数据filter过滤条件
        #.filter(Lagoutables.crawl_date==self.date).all()

        result_list1 = [x[0].split(',')[0] for x in result]#只取第一个标签
        result_list2 = [x for x in Counter(result_list1).items() if x[1]>150]#Counter标签计数字典类型Counter({'移动互联网': 848, '企业服务': 160})
        # #填充的是series里面的data
        data = [{"name":x[0],"value":x[1]} for x in result_list2]
        name_list = [name['name'] for name in data]
        info['x_name'] = name_list
        info['data'] = data
        return info

    # 查询薪资情况
    def query_salary_result(self):
        info = {}
        # 查询今日抓取到的薪资数据
        result = self.mysql_session.query(Lagoutables.salary).all()
        #.filter(Lagoutables.crawl_date==self.date).all()#过滤
        # 处理原始数据
        result_list1 = [x[0] for x in result]
        # 计数,并返回
        result_list2 = [x for x in Counter(result_list1).items() if x[1]>100]
        result = [{"name": x[0], "value": x[1]} for x in result_list2]
        name_list = [name['name'] for name in result]
        info['x_name'] = name_list
        info['data'] = result
        return info

    # 查询工作年限情况
    def query_workyear_result(self):
        info = {}
        # 查询今日抓取到的薪资数据
        result = self.mysql_session.query(Lagoutables.workYear).all()
        #filter(Lagoutables.crawl_date==self.date).all()过滤
        # 处理原始数据
        result_list1 = [x[0] for x in result]
        # 计数,并返回
        result_list2 = [x for x in Counter(result_list1).items()]
        result = [{"name": x[0], "value": x[1]} for x in result_list2 if x[1]>15]
        name_list = [name['name'] for name in result]
        info['x_name'] = name_list
        info['data'] = result
        return info

    # 查询学历信息
    def query_education_result(self):
        info = {}
        # 查询今日抓取到的薪资数据
        result = self.mysql_session.query(Lagoutables.education).all()
        #.filter(Lagoutables.crawl_date==self.date).all()过滤
        # 处理原始数据
        result_list1 = [x[0] for x in result]
        # 计数,并返回
        result_list2 = [x for x in Counter(result_list1).items()]
        result = [{"name": x[0], "value": x[1]} for x in result_list2]
        name_list = [name['name'] for name in result]
        info['x_name'] = name_list
        info['data'] = result
        return info

    # 岗位发布数量,折线图
    def query_job_result(self):
        info = {}
        result = self.mysql_session.query(Lagoutables.crawl_date,func.count('*').label('c')).group_by(Lagoutables.crawl_date).all()
        result1 = [{"name": x[0], "value": x[1]} for x in result]
        name_list = [name['name'] for name in result1]
        info['x_name'] = name_list
        info['data'] = result1
        return info

    # 根据城市计数
    def query_city_result(self):
        info = {}
        # 查询今日抓取到的薪资数据
        result = self.mysql_session.query(Lagoutables.city,func.count('*').label('c')).group_by(Lagoutables.city).all()
        # result = self.mysql_session.query(Lagoutables.city,func.count('*').label('c')).filter(Lagoutables.crawl_date==self.date).group_by(Lagoutables.city).all()
        result1 = [{"name": x[0], "value": x[1]} for x in result]
        name_list = [name['name'] for name in result1]
        info['x_name'] = name_list
        info['data'] = result1
        return info

    #融资情况
    def query_financestage_result(self):
        info = {}
        # 查询今日抓取到的薪资数据
        result = self.mysql_session.query(Lagoutables.financeStage).all()
       #.filter(Lagoutables.crawl_date == self.date).all()#过滤条件
        # 处理原始数据
        result_list1 = [x[0] for x in result]
        # 计数,并返回
        result_list2 = [x for x in Counter(result_list1).items()]
        result = [{"name": x[0], "value": x[1]} for x in result_list2]
        name_list = [name['name'] for name in result]
        info['x_name'] = name_list
        info['data'] = result
        return info

    # 公司规模
    def query_companysize_result(self):
        info = {}
        # 查询今日抓取到的薪资数据
        result = self.mysql_session.query(Lagoutables.companySize).all()
        #.filter(Lagoutables.crawl_date == self.date).all()过滤条件
        # 处理原始数据
        result_list1 = [x[0] for x in result]
        # 计数,并返回
        result_list2 = [x for x in Counter(result_list1).items()]
        result = [{"name": x[0], "value": x[1]} for x in result_list2]
        name_list = [name['name'] for name in result]
        info['x_name'] = name_list
        info['data'] = result
        return info


    # 任职情况
    def query_jobNature_result(self):
        info = {}
        # 查询今日抓取到的薪资数据
        result = self.mysql_session.query(Lagoutables.jobNature).all()
        #.filter(Lagoutables.crawl_date == self.date).all()#过滤条件
        # 处理原始数据
        result_list1 = [x[0] for x in result]
        # 计数,并返回
        result_list2 = [x for x in Counter(result_list1).items()]
        result = [{"name": x[0], "value": x[1]} for x in result_list2]
        name_list = [name['name'] for name in result]
        info['x_name'] = name_list
        info['data'] = result
        return info

    # 抓取数量
    def count_result(self):
        info = {}
        info['all_count'] = self.mysql_session.query(Lagoutables).count()
        info['today_count'] = self.mysql_session.query(Lagoutables).count()
       #.filter(Lagoutables.crawl_date==self.date).count()过滤条件
        return info




lagou_mysql = HandleLagouData()
