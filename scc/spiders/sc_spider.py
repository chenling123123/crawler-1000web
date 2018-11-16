#coding=utf8

import scrapy
from scrapy import Request
from scc.read_config_warehouses.read_json import read_config
import os
from scrapy.selector import Selector
from scc.items import SccLastItem,SccListItem
from scc.public_warehouses.date_clean import filter
from scc.public_warehouses.creat_uuid_32 import uuid_32
from scc.public_warehouses.pick_time import pickTime
from scc.download_warehouses.download import download
from scc.public_warehouses.interception_meth import interception
from scc.sql_warehouses.list_sql_duplicate_removal import duplicate_removal
from scc.public_warehouses.url_clean import url_join
class  ScSpider(scrapy.Spider):
    name = "scSpider"

    def __init__(self):
        self.config_id=""
        self.read_list_config=read_config()
        self.list_config=''
        self.detail_config=''
        self.data_source_name=''
        self.data_source_type=''
        self.web_type = ''
        self.category = ''
        self.web_column = ''
        self.id_generator = uuid_32()
        self.pick_time_generator = pickTime()
        self.interception=interception()
        self.download_generator=download()
        self.duplicate_removal_generator=duplicate_removal()
        self.urljoin=url_join()


    def start_requests(self):
        for filenames in os.walk(os.path.dirname(os.getcwd())+'/scc/scc/config/list_json_config'):
            for filename in filenames[2]:

                self.config_id = filename
                self.list_config=self.read_list_config.read_list_config_json(os.path.dirname(os.getcwd())+'/scc/scc/config/list_json_config/'+self.config_id)
                self.detail_config=self.read_list_config.read_details_config_json(os.path.dirname(os.getcwd())+'/scc/scc/config/details_json_config/'+self.config_id)
                # self.list_config = self.read_list_config.read_list_config_json(
                #     os.path.dirname(os.getcwd()) + '/scc/scc/config/list_json_config/' + "1036.json")
                # self.detail_config = self.read_list_config.read_details_config_json(
                #     os.path.dirname(os.getcwd()) + '/scc/scc/config/details_json_config/' + '1036.json')

                self.data_source_name=self.list_config['data_source_name']
                self.data_source_type=self.list_config['data_source_type']
                self.web_type = self.list_config['web_type']
                self.category = self.list_config['category']
                self.web_column = self.list_config['web_column']
                start_url=self.list_config['start_url']
                url_list=[]
                url_list.append(start_url)
                #self.list_duplicate_num=0
                if self.list_config['order']==0:
                    if self.list_config['first_page_num']=="":
                        yield Request(url=start_url, meta={"urllist": start_url},callback=self.parse, encoding='utf-8')
                    else:
                        for i in range(int(self.list_config['first_page_num']),int(self.list_config['last_page_num'])+1,int(self.list_config['gap'])):
                            url_list.append(self.list_config['url'] % i)
                        for url in url_list:
                            #url判断去重

                            yield Request(url=url, meta={"urllist": url},callback=self.parse, encoding='utf-8')

                elif self.list_config['order']==1:
                    if self.list_config['first_page_num']=="":
                        yield Request(url=start_url, meta={"urllist": start_url},callback=self.parse, encoding='utf-8')
                    else:

                        for i in range(int(self.list_config['first_page_num']),int(self.list_config['last_page_num'])+1,int(self.list_config['gap']))[::-1]:
                            url_list.append(self.list_config['url'] % i)
                        for url in url_list:
                            #url判断去重

                            yield Request(url=url, meta={"urllist": url},callback=self.parse, encoding='utf-8')

    def parse(self, response):
        item = SccListItem()
        list_dataClean = filter()
        title_last=""
        pub_time_last=''
        if self.list_config['web_format']=='html':
            sel=Selector(response=response).xpath(self.list_config['body_xpath']).extract()
            for se in sel:
                try:
                    if len(Selector(text=se).xpath(self.list_config['url_xpath']).extract())>0:
                        url=Selector(text=se).xpath(self.list_config['url_xpath']).extract()[0].replace('%20','')
                        # url处理
                        if url[0:4] == "http":
                            pass
                        else:
                            if self.list_config['details_url_type']=='get_list':

                                url=self.urljoin.joinurl(response.meta["urllist"],url)
                            elif self.list_config['details_url_type']=='get_str':
                                url=self.list_config['details_url'] % url
                    else:
                        print('该列表中没有找到url:'+str(Selector(text=se).xpath(self.list_config['url_xpath']).extract()))
                        continue
                except Exception:
                    raise Exception
                if self.list_config['pub_time']=="":
                    pass
                else:
                    if len(Selector(text=se).xpath(self.list_config['pub_time']).extract())>0:

                        pub_time=Selector(text=se).xpath(self.list_config['pub_time']).extract()[0]

                        pub_time_last = list_dataClean.date_clean(pub_time)
                        pub_time_last = list_dataClean.clean_mark(pub_time_last)
                    else:
                        print("该列表页中没有找到时间")
                        continue
                item['url'] = url
                item['state'] = 0
                item['id'] = self.id_generator.creat_uuid()
                if self.duplicate_removal_generator.judge_duplicate(url) == 0:

                    yield item
                    yield Request(url=url, meta={"url": url, 'pub_time_last' : pub_time_last, "title_last":title_last}, callback=self.parse_details,encoding='utf-8')
                else:

                    print("网站已采集"+url)
                    pass
        elif self.list_config['web_format']=='json':
            text=response.text
            try:
                if len(self.interception.str_interception(text, self.list_config['interception_body_first'], self.list_config['interception_body_last']))>0:
                    body=self.interception.str_interception(text, self.list_config['interception_body_first'], self.list_config['interception_body_last'])[0]
                    body_lists=self.interception.str_interception(body, self.list_config['interception_list_first'], self.list_config['interception_list_last'])
                    for body_list in body_lists:
                        if len(self.interception.str_interception(body_list, self.list_config['interception_url_first'], self.list_config['interception_url_last']))>0:
                            url=self.interception.str_interception(body_list, self.list_config['interception_url_first'], self.list_config['interception_url_last'])[0]

                            if url[0:4] == "http":
                                pass
                            else:
                                if self.list_config['details_url_type'] == 'get_list':

                                    url = self.urljoin.joinurl(response.meta["urllist"], url)
                                elif self.list_config['details_url_type'] == 'get_str':
                                    url = self.list_config['details_url'] % url
                            if self.list_config['interception_pub_time_first']=="":
                                pass
                            else:
                                print(body_list)
                                pub_time_last=self.interception.str_interception(body_list, self.list_config['interception_pub_time_first'], self.list_config['interception_pub_time_last'])[0]
                                pub_time_last=list_dataClean.date_clean(pub_time_last)
                                pub_time_last = list_dataClean.clean_mark(pub_time_last)
                            if ('interception_title_first' in self.list_config):
                                title_last= self.interception.str_interception(body_list, self.list_config['interception_title_first'], self.list_config['interception_title_last'])[0]
                                title_last = list_dataClean.clean_mark_content(title_last)
                            else:
                                pass
                            item['url'] = url
                            item['state'] = 0
                            item['id'] = self.id_generator.creat_uuid()
                            if self.duplicate_removal_generator.judge_duplicate(url) == 0:
                                yield item
                                yield Request(url=url, meta={"url": url, 'pub_time_last' : pub_time_last, "title_last":title_last}, callback=self.parse_details,encoding='utf-8')
                            else:

                                print("网站已采集"+url)
            except Exception:
                raise Exception

    def parse_details(self, response):
        dataClean=filter()
        item=SccLastItem()
        downloadMeth=download()
        item['url']=response.meta["url"]
        item['data_source_name']=self.data_source_name
        item['data_source_type'] = self.data_source_type
        item['web_type'] = self.web_type
        item['category'] = self.category
        item['web_column'] = self.web_column
        item['id'] = self.id_generator.creat_uuid()
        #标题字段采集
        title_type_size=self.detail_config['title_xpath']['type_size']
        title_last = response.meta['title_last']
        if title_last=="":
            if title_type_size==0:
                pass
            else:
                for i in range(title_type_size):
                    title_list=Selector(response=response).xpath(self.detail_config['title_xpath']['xpath'+str(i)]).extract()

                    title_list_last=''.join(title_list)
                    text=dataClean.clean_mark_content(title_list_last)

                    if text!="":
                        title_last=text
                        break
            if title_last == "":
                if ('interception_first' in self.detail_config['title_xpath']):
                    text = response.text
                    if len(self.interception.str_interception(text,
                                                              self.detail_config['title_xpath']['interception_first'],
                                                              self.detail_config['title_xpath']['interception_last'])):
                        title = self.interception.str_interception(text, self.detail_config['title_xpath']['interception_first'], self.detail_config['title_xpath']['interception_last'])[0]
                        title_last = dataClean.clean_mark_content(title)
                    else:
                        print('截取的字段为空')
                else:
                    print("title为空或配置文件不全")
        else:
            title_last=dataClean.clean_mark_content(title_last)
        # 发布时间字段采集
        pub_time_size=self.detail_config['pub_time_xpath']['type_size']
        pub_time_last = response.meta['pub_time_last']
        if pub_time_last =='':
            if pub_time_size==0:
                pass
            else:
                for i in range(pub_time_size):
                    pub_time_list=Selector(response=response).xpath(self.detail_config['pub_time_xpath']['xpath'+str(i)]).extract()
                    pub_time_list_last=''.join(pub_time_list)
                    print(pub_time_list_last)
                    pub_time=dataClean.clean_mark(pub_time_list_last)
                    if pub_time != "":
                        #pub_time_last =pub_time
                        pub_time_last=dataClean.date_clean(pub_time)
                        break
            if pub_time_last == "":
                if ('interception_first' in self.detail_config['pub_time_xpath']):
                    text = response.text
                    if len(self.interception.str_interception(text,
                                                              self.detail_config['pub_time_xpath']['interception_first'],
                                                              self.detail_config['pub_time_xpath']['interception_last'])):
                        pub_time = self.interception.str_interception(text, self.detail_config['pub_time_xpath']['interception_first'], self.detail_config['pub_time_xpath']['interception_last'])[0]
                        pub_time_last = dataClean.date_clean(pub_time)
                        pub_time_last = dataClean.clean_mark(pub_time_last)
                    else:
                        print('截取的字段为空')
                else:
                    print("pub_time为空或配置文件不全")
        else:
            pub_time_last = dataClean.clean_mark(pub_time_last)
        # 正文字段采集
        content_size=self.detail_config['content_xpath']['type_size']
        content_last=''
        if content_size==0:
            pass
        else:
            for i in range(content_size):
                content_list=Selector(response=response).xpath(self.detail_config['content_xpath']['xpath'+str(i)]).extract()
                content_list_last=''.join(content_list)
                content = dataClean.clean_mark_content(content_list_last)
                if content != "":
                    content_last = content
                    #print(content_last)
                    break
        if content_last =="":
            if ('interception_first' in self.detail_config['content_xpath']):

                text = response.text
                if len(self.interception.str_interception(text, self.detail_config['content_xpath']['interception_first'], self.detail_config['content_xpath']['interception_last'])):
                    content = self.interception.str_interception(text, self.detail_config['content_xpath']['interception_first'], self.detail_config['content_xpath']['interception_last'])[0]
                    content_last = dataClean.clean_mark_content(content)
                else:
                    print('截取的字段为空')
            else:
                print("content为空或配置文件不全")
        # 发文字号字段采集
        issued_number_size = self.detail_config['issued_number_xpath']['type_size']
        issued_number_last=""
        if issued_number_size==0:
            pass
        else:
            for i in range(issued_number_size):
                issued_number_list=Selector(response=response).xpath(self.detail_config['issued_number_xpath']['xpath'+str(i)]).extract()
                issued_number_list_last=''.join(issued_number_list)
                issued_number=dataClean.clean_mark(issued_number_list_last)
                if issued_number !="":
                    issued_number_last=issued_number
                    break
        if issued_number_last == "":
            if ('interception_first' in self.detail_config['issued_number_xpath']):
                text = response.text
                if len(self.interception.str_interception(text,
                                                          self.detail_config['issued_number_xpath']['interception_first'],
                                                          self.detail_config['issued_number_xpath']['interception_last'])):
                    issued_number = self.interception.str_interception(text, self.detail_config['issued_number_xpath']['interception_first'],
                                                       self.detail_config['issued_number_xpath']['interception_last'])[0]
                    issued_number_last = dataClean.clean_mark(issued_number)
                else:
                    print('截取的字段为空')
            else:
                print("issued_number为空或配置文件不全")

        # 来源字段采集
        content_source_size = self.detail_config['content_source_xpath']['type_size']
        content_source_last = ""
        if content_source_size==0:
            pass
        else:
            for i in range(content_source_size):
                content_source_list = Selector(response=response).xpath(self.detail_config['content_source_xpath']['xpath'+str(i)]).extract()
                content_source_list_last=''.join(content_source_list)
                content_source = dataClean.clean_mark_content(content_source_list_last)
                if content_source != "":
                    content_source_last = content_source
                    break
        if content_source_last=="":
            if ('interception_first' in self.detail_config['content_source_xpath']):
                text = response.text
                if len(self.interception.str_interception(text,
                                                          self.detail_config['content_source_xpath']['interception_first'],
                                                          self.detail_config['content_source_xpath']['interception_last'])):
                    content_source = self.interception.str_interception(text, self.detail_config['content_source_xpath']['interception_first'],
                                                       self.detail_config['content_source_xpath']['interception_last'])[0]
                    content_source_last = dataClean.clean_mark_content(content_source)
                else:
                    print('截取的字段为空')
            else:
                print("content_source为空或配置文件不全")
        #print(content_source_last)
        # 发布单位字段采集
        issued_unit_size = self.detail_config['issued_unit_xpath']['type_size']
        issued_unit_last = ""

        if issued_unit_size==0:
            pass
        else:
            for i in range(issued_unit_size):
                issued_unit_list = Selector(response=response).xpath(self.detail_config['issued_unit_xpath']['xpath'+str(i)]).extract()
                issued_unit_list_last = ''.join(issued_unit_list)
                issued_unit = dataClean.clean_mark(issued_unit_list_last)
                if issued_unit != "":
                    issued_unit_last=issued_unit
                    break
        if issued_unit_last=="":
            if ('interception_first' in self.detail_config['issued_unit_xpath']):
                text = response.text
                if len(self.interception.str_interception(text,
                                                          self.detail_config['issued_unit_xpath']['interception_first'],
                                                          self.detail_config['issued_unit_xpath']['interception_last'])):
                    issued_unit = self.interception.str_interception(text, self.detail_config['issued_unit_xpath']['interception_first'],
                                                       self.detail_config['issued_unit_xpath']['interception_last'])[0]
                    issued_unit_last = dataClean.clean_mark(issued_unit)
                else:
                    print('截取的字段为空')
            else:
                print("content_source为空或配置文件不全")
        item['title'] = dataClean.delete_label(title_last)
        item['pick_time'] = self.pick_time_generator.creat_pick_time()
        #正文中图片，附件，视频下载并清洗
        item['pub_time'] = dataClean.delete_label(pub_time_last)
        if item['pub_time']=="":
            pass
        else:

            if dataClean.contrast(item['pub_time']) or int(item['pub_time'][0:4])<2018:
                pass
            else:
                content_last, item['img_path'] = self.download_generator.img_download(content_last, item['pick_time'],
                                                                                      item['url'])
                if len(item['img_path'])>1024:
                    print('长度出错'+item['img_path'])
                else:

                    content_last, item['attachment_path'] = self.download_generator.attachment_download(content_last,
                                                                                                        item['pick_time'],
                                                                                                        item['url'])
                    content_last, item['media_path'] = self.download_generator.media_download(content_last,
                                                                                              item['pick_time'],
                                                                                              item['url'])
                    item['content'] = content_last

                    item['issued_number'] = dataClean.delete_label(issued_number_last)
                    item['content_source'] = dataClean.delete_label(content_source_last)
                    item['issued_unit'] = dataClean.delete_label(issued_unit_last)
                    if item['content'] == '' or item['title'] == '':
                        pass
                    else:
                        yield item