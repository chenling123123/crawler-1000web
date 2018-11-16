from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime,Text,TIMESTAMP
from sqlalchemy.orm import sessionmaker
import configparser
import os
from scc.read_config_warehouses.read_ini import read_config


readConfig = read_config()
sql_model=readConfig.read_config_ini()
user=sql_model.user
password=sql_model.password
host=sql_model.host
db=sql_model.db
engine = create_engine('mysql+pymysql://'+user+':'+password+'@'+host+'/'+db+'?charset=utf8')

Base = declarative_base()
class list_item(Base):
    __tablename__ = 'busi_no_quality_data_list'
    id = Column(String(32), primary_key=True)
    url = Column(String(255))
    state = Column(Integer, default=0)


class details_item(Base):
    __tablename__ = 'busi_no_quality_data'
    id = Column(String(32), primary_key=True)
    title = Column(String(255))
    pub_time = Column(String(50))
    pick_time = Column(String(50))
    url = url = Column(String(255))
    data_source_name = Column(String(50))
    data_source_type = Column(String(2))
    web_type = Column(String(50))
    web_column=Column(String(50))
    category = Column(String(50))
    content = Column(Text)
    img_path = Column(String(255))
    attachment_path = Column(String(255))
    media_path=Column(String(255))
    issued_number=Column(String(50))
    content_source=Column(String(50))
    issued_unit=Column(String(50))