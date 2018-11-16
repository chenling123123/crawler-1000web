import pymysql
from scc.read_config_warehouses.read_ini import read_config
class read_sql():
    def __init__(self):

        self.config = read_config()
        self.sql_model = self.config.read_config_ini()
        self.host = self.sql_model.host
        self.user = self.sql_model.user
        self.password = self.sql_model.password
        self.db = self.sql_model.db
    def read_sql_config(self):
        pass

    def read_config(self,basic_type,basic_value):

        db = pymysql.connect(host=self.host, user=self.user,
                             password=self.password, db=self.db, port=3306)

        cur = db.cursor()

        sql = "select basic_name from sys_basic_data where basic_type= "+"'"+"%s"+"'"+" and basic_value="+"'"+"%s"+"'"
        try:
            cur.execute(sql % (basic_type,basic_value))
            results = cur.fetchall()
            return results[0][0]
        except Exception:
            raise Exception
        finally:
            db.close()

if __name__ == '__main__':
    read=read_sql()
    print(read.read_config('imgPathReplace','1'))