import os
import json

class read_config():
    def __init__(self):
        pass
    #读列表页配置文件
    def read_list_config_json(self, path):

            if os.path.isfile(path):
                try:
                    with open(path, 'r', encoding='UTF-8') as f:
                        duty = json.load(f)
                        return duty
                except Exception as e:
                    print("%s列表页配置文件格式有误,原因：%s" % (path, e))
    #读详情页配置文件
    def read_details_config_json(self, path):
        if os.path.isfile(path):
            try:
                with open(path, 'r', encoding='UTF-8') as f:
                    duty = json.load(f)
                    return duty
            except Exception as e:
                print("%s详情页配置文件格式有误,原因：%s" % (path, e))
if __name__ == '__main__':
    setting=read_config.read_list_config_json(11,os.path.dirname(os.getcwd())+'/config/list_json_config/1.json')

    print(os.path.dirname(os.getcwd())+'/config/list_json_config/1.json')
    print(setting['url'])