from scrapy import cmdline
import os, time
from scc.read_config_warehouses.read_sql import read_sql
# for filenames in os.walk('/home/chenling/Documents/python_project/scc/scc/config/list_json_config'):
#     print(type(filenames[2]),len(filenames[2]))
#     for filename in filenames[2]:
#         #print(filename)
#         pass

ISOTIMEFORMAT = '%Y-%m-%d %X'
picktime = str(time.strftime(ISOTIMEFORMAT, time.localtime()))
picktime = picktime.replace('-', '')
year = picktime[0:4]
month = picktime[4:6]
date = picktime[6:8]
readSql=read_sql()
# logger.setLevel(logging.DEBUG)
path = readSql.read_config("crawlerLogPath","1")

print(path)
dir_name=os.path.join(path,year)
dir_name=os.path.join(dir_name,month)
dir_name=os.path.join(dir_name,date)

if not os.path.exists(dir_name):
    os.makedirs(dir_name)
command="scrapy crawl scSpider -s LOG_FILE="+dir_name+"/log"
#command="scrapy crawl scSpider"
cmdline.execute(command.split())
