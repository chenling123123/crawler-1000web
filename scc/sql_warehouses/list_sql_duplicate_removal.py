import pymysql
from scc.read_config_warehouses.read_ini import read_config

class duplicate_removal():
    def __init__(self):

        self.config = read_config()
        self.sql_model = self.config.read_config_ini()
        self.host = self.sql_model.host
        self.user = self.sql_model.user
        self.password = self.sql_model.password
        self.db = self.sql_model.db
    #列表页数据判断去重 0.不重复 1.重复
    def judge_duplicate(self,url):
        db = pymysql.connect(host=self.host, user=self.user,
                             password=self.password, db=self.db, port=3306)

        cur = db.cursor()

        sql = "select count(*) from busi_no_quality_data_list where url= "+"'"+"%s"+"'"

        try:

            count=cur.execute(sql % (url))
            results = cur.fetchall()
            return results[0][0]
        except Exception:
            raise Exception
        finally:
            db.close()
        return 0

if __name__ == '__main__':
    read = duplicate_removal()
    print(read.judge_duplicate('www.asdfs.com'))