import configparser
import os
from scc.model.models import sql_connect_model
class read_config():
    #数据库链接信息
    def read_config_ini(self):
        # try:
            config=configparser.ConfigParser()
            config.read(os.path.dirname(os.getcwd())+"/scc/scc/config/sql_connect_config/config.ini")

            user=config.get("database","user")
            password=config.get("database","password")
            host=config.get("database","host")
            db=config.get("database","db")
            sql_model=sql_connect_model(user,password,host,db)
            return sql_model
        # except Exception as e:
        #     print("数据库链接出错" % e)

if __name__ == '__main__':
    config=read_config()
    host=config.read_config_ini().host
    print(host)