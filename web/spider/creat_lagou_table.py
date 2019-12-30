from sqlalchemy import create_engine,Integer,Float,String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
engine=create_engine("mysql+pymysql://root:password@ip:3306/lagou?charset=utf8")
Session=sessionmaker(bind=engine)#创建数据库seesion
Base=declarative_base()#申明基类
class Lagoutables(Base):
    __tablename__='lagou_data'#表明

    id=Column(Integer,primary_key=True,autoincrement=True)#主键自动增长

    positionId=Column(Integer,nullable=True)#岗位id非空

    longitude = Column(Float, nullable=False)  # 经度

    latitude = Column(Float, nullable=False) # 纬度

    positionName = Column(String(length=50), nullable=False) # 岗位名称

    workYear = Column(String(length=20), nullable=False)  # 工作年限

    education = Column(String(length=20), nullable=False) # 学历

    jobNature = Column(String(length=20), nullable=True)  # 岗位性质

    financeStage = Column(String(length=30), nullable=True)   # 公司类型

    companySize = Column(String(length=30), nullable=True)  # 公司规模

    industryField = Column(String(length=30), nullable=True)  # 业务方向

    city = Column(String(length=10), nullable=False)  # 所在城市

    positionAdvantage = Column(String(length=200), nullable=True)  # 岗位标签

    companyShortName = Column(String(length=50), nullable=True)  # 公司简称

    companyFullName = Column(String(length=200), nullable=True)  # 公司全称

    district = Column(String(length=20), nullable=True)  # 公司所在区

    companyLabelList = Column(String(length=200), nullable=True)   # 公司福利标签

    salary = Column(String(length=20), nullable=False) # 工资

    crawl_date = Column(String(length=20), nullable=False) # 抓取日期


if __name__ == '__main__':
    # 创建数据表
    Lagoutables.metadata.create_all(engine)