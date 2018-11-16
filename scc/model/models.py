
#数据库链接配置文件
class sql_connect_model():
    def __init__(self, user, password, host, db):
        self.user=user
        self.password = password
        self.host = host
        self.db = db
#列表页配置文件
class json_model_list():
    def __init__(self, start_url, url, list_num, content_xpath, tag):
        self.start_url = start_url
        self.url = url
        self.list_num = list_num
        self.content_xpath = content_xpath
        self.tag = tag
#详情页配置文件
class json_model_details():
    def __init__(self, title_xpath, content_xpath, issued_number_xpath, pub_time_xpath, content_source_xpath, issued_unit_xpath, data_source_name, data_source_type, web_type, category):
        self.title_xpath = title_xpath
        self.content_xpath = content_xpath
        self.issued_number_xpath = issued_number_xpath
        self.pub_time_xpath = pub_time_xpath
        self.content_source_xpath = content_source_xpath
        self.issued_unit_xpath = issued_unit_xpath
        self.data_source_name = data_source_name
        self.data_source_type = data_source_type
        self.web_type = web_type
        self.category = category

