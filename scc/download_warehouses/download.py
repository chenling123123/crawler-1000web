import os, re, uuid
import urllib
import configparser
from scc.read_config_warehouses.read_sql import read_sql
from scc.read_config_warehouses.read_ini import read_config
from scc.public_warehouses.url_clean import url_join
class download():
    def __init__(self):
        self.readSql=read_sql()
        self.config = read_config()
        self.sql_model=self.config.read_config_ini()
        self.host = self.sql_model.host
        self.user = self.sql_model.user
        self.password = self.sql_model.password
        self.db = self.sql_model.db
        self.urljoin=url_join()
    def img_download(self, content_last, pickTime, url):
        imgs = re.findall("<img.*?>", content_last)
        picktime = pickTime
        year = picktime[0:4]
        month = picktime[5:7]
        date = picktime[8:10]
        imgpathslist = []
        imgurllist = []
        if len(imgs) > 0:
            for img in imgs:

                imguid = uuid.uuid1()
                imguid = str(imguid).replace('-', '')
                src_list = re.findall('src="(.*?)"', img)
                for src in src_list:
                    print("原文src："+src)
                    if src[0:4] == "http":
                        imgurl = src
                    else:
                        imgurl=self.urljoin.joinurl(url,src)
                        #########
                    print("处理后的src："+imgurl)
                    # dir_name = self.readSql.read_config('imgDownloadPath', '1')
                    # dir_name = os.path.join(dir_name, "image")
                    # dir_name = os.path.join(dir_name, year)
                    # dir_name = os.path.join(dir_name, month)
                    # dir_name = os.path.join(dir_name, date)
                    # serverimgpath1=self.readSql.read_config('imgPathReplace', '1')
                    # serverimgpath1=os.path.join(serverimgpath1,"image")
                    # serverimgpath1=os.path.join(serverimgpath1,year)
                    # serverimgpath1=os.path.join(serverimgpath1,month)
                    # serverimgpath1=os.path.join(serverimgpath1,date)
                    # if not os.path.exists(dir_name):
                    #     os.makedirs(dir_name)
                    #
                    # if len(re.findall("png", src)) > 0:
                    #     filename = os.path.join(dir_name, imguid + '.png')
                    #     serverimgpath1 = os.path.join(imguid + '.png')
                    # elif len(re.findall("PNG", src)) > 0:
                    #     filename = os.path.join(dir_name, imguid + '.PNG')
                    #     serverimgpath1 = os.path.join(imguid + '.PNG')
                    # elif len(re.findall("jpg", src)) > 0:
                    #     filename = os.path.join(dir_name, imguid + '.jpg')
                    #     serverimgpath1 = os.path.join(imguid + '.jpg')
                    # elif len(re.findall("JPG", src)) > 0:
                    #     filename = os.path.join(dir_name, imguid + '.JPG')
                    #     serverimgpath1 = os.path.join(imguid + '.JPG')
                    # elif len(re.findall("gif", src)) > 0:
                    #     filename = os.path.join(dir_name, imguid + '.gif')
                    #     serverimgpath1 = os.path.join(imguid + '.gif')
                    # elif len(re.findall("GIF", src)) > 0:
                    #     filename = os.path.join(dir_name, imguid + '.GIF')
                    #     serverimgpath1 = os.path.join(imguid + '.GIF')
                    # elif len(re.findall("jpeg", src)) > 0:
                    #     filename = os.path.join(dir_name, imguid + '.jpeg')
                    #     serverimgpath1 = os.path.join(imguid + '.jpeg')
                    # elif len(re.findall("JPEG", src)) > 0:
                    #     filename = os.path.join(dir_name, imguid + '.JPEG')
                    #     serverimgpath1 = os.path.join(imguid + '.JPEG')
                    #
                    # elif len(re.findall("bmp", src)) > 0:
                    #     filename = os.path.join(dir_name, imguid + '.bmp')
                    #     serverimgpath1 = os.path.join(imguid + '.bmp')
                    # elif len(re.findall("BMP", src)) > 0:
                    #     filename = os.path.join(dir_name, imguid + '.BMP')
                    #     serverimgpath1 = os.path.join(imguid + '.BMP')
                    #
                    # opener = urllib.request.build_opener()
                    # opener.addheaders = [('User-Agent',
                    #                       'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36')]
                    # urllib.request.install_opener(opener)

                    try:
                        #urllib.request.urlretrieve(imgurl, filename)
                        content_last = content_last.replace(src, imgurl)

                    except:
                        filename = "无效的图片路径"
                        print("无效的图片路径：" + imgurl)
                        #self.logger.info("无效的图片路径：%s", imgurl)
                    imgpathslist.append(imgurl)
                return content_last,str(imgpathslist)
        else:
            return content_last,str(imgpathslist)
    def media_download(self, content_last, pickTime, url):
        a_list = re.findall("<video.*?>", content_last)
        picktime = pickTime
        year = picktime[0:4]
        month = picktime[5:7]
        date = picktime[8:10]
        medialist = []
        date = date
        if len(a_list) > 0:
            for a in a_list:
                imguid = uuid.uuid1()
                imguid = str(imguid).replace('-', '')
                src_list = re.findall('href="(.*?)"', a)
                for src in src_list:
                    if src[0:4] == "http":
                        mediaurl = src
                    else:
                        mediaurl = self.urljoin.joinurl(url, src)

                    # dir_name = self.readSql.read_config('mediaDownloadPath', '1')
                    # dir_name = os.path.join(dir_name, "media")
                    # dir_name = os.path.join(dir_name, year)
                    # dir_name = os.path.join(dir_name, month)
                    # dir_name = os.path.join(dir_name, date)
                    # serverimgpath1=self.readSql.read_config('mediaPathReplace', '1')
                    # serverimgpath1=os.path.join(serverimgpath1,"media")
                    # serverimgpath1=os.path.join(serverimgpath1,year)
                    # serverimgpath1=os.path.join(serverimgpath1,month)
                    # serverimgpath1=os.path.join(serverimgpath1,date)
                    # if not os.path.exists(dir_name):
                    #     os.makedirs(dir_name)
                    # if len(re.findall("mp4", src)) > 0:
                    #     filename = os.path.join(dir_name, imguid + '.mp4')
                    #     serverimgpath1 = os.path.join(imguid + '.mp4')
                    # elif len(re.findall("vob", src)) > 0:
                    #     filename = os.path.join(dir_name, imguid + '.vob')
                    #     serverimgpath1 = os.path.join(imguid + '.vob')
                    # elif len(re.findall("ifo", src)) > 0:
                    #     filename = os.path.join(dir_name, imguid + '.ifo')
                    #     serverimgpath1 = os.path.join(imguid + '.ifo')
                    # elif len(re.findall("mpg", src)) > 0:
                    #     filename = os.path.join(dir_name, imguid + '.mpg')
                    #     serverimgpath1 = os.path.join(imguid + '.mpg')
                    # elif len(re.findall("mpeg", src)) > 0:
                    #     filename = os.path.join(dir_name, imguid + '.mpeg')
                    #     serverimgpath1 = os.path.join(imguid + '.mpeg')
                    # elif len(re.findall("dat", src)) > 0:
                    #     filename = os.path.join(dir_name, imguid + '.dat')
                    #     serverimgpath1 = os.path.join(imguid + '.dat')
                    # elif len(re.findall("3gp", src)) > 0:
                    #     filename = os.path.join(dir_name, imguid + '.3gp')
                    #     serverimgpath1 = os.path.join(imguid + '.3gp')
                    # elif len(re.findall("rm", src)) > 0:
                    #     filename = os.path.join(dir_name, imguid + '.rm')
                    #     serverimgpath1 = os.path.join(imguid + '.rm')
                    # elif len(re.findall("mov", src)) > 0:
                    #     filename = os.path.join(dir_name, imguid + '.mov')
                    #     serverimgpath1 = os.path.join(imguid + '.mov')
                    # elif len(re.findall("ram", src)) > 0:
                    #     filename = os.path.join(dir_name, imguid + '.ram')
                    #     serverimgpath1 = os.path.join(imguid + '.ram')
                    # elif len(re.findall("rmvb", src)) > 0:
                    #     filename = os.path.join(dir_name, imguid + '.rmvb')
                    #     serverimgpath1 = os.path.join(imguid + '.rmvb')
                    # elif len(re.findall("wmv", src)) > 0:
                    #     filename = os.path.join(dir_name, imguid + '.wmv')
                    #     serverimgpath1 = os.path.join(imguid + '.wmv')
                    # else:
                    #     continue
                    # opener = urllib.request.build_opener()
                    # opener.addheaders = [('User-Agent',
                    #                       'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36')]
                    # urllib.request.install_opener(opener)

                    try:
                        #urllib.request.urlretrieve(mediaurl, filename)
                        content_last = content_last.replace(src, mediaurl)

                    except:
                        filename = "无效的附件路径"
                        print("无效的附件路径：" + mediaurl)
                        #self.logger.info("无效的附件路径：%s", mediaurl)
                    medialist.append(mediaurl)
                return content_last, str(medialist)
        else:
            return content_last, str(medialist)
    def attachment_download(self, content_last, pickTime, url):
        a_list1 = re.findall("<a.*?>", content_last)
        a_list2 = re.findall("<embed.*?>", content_last)
        a_list = a_list1+a_list2
        picktime = pickTime
        year = picktime[0:4]
        month = picktime[5:7]
        date = picktime[8:10]
        attachmentlist = []

        date = date
        if len(a_list) > 0:
            for a in a_list:

                imguid = uuid.uuid1()
                imguid = str(imguid).replace('-', '')
                src_list1 = re.findall('href="(.*?)"', a)
                src_list2 = re.findall('src="(.*?)"', a)
                src_list=src_list1+src_list2
                for src in src_list:

                    if src[0:4] == "http":
                        attachmenturl = src
                    else:
                        attachmenturl = self.urljoin.joinurl(url, src)

                    # dir_name = self.readSql.read_config('attachmentDownloadPath', '1')
                    # dir_name = os.path.join(dir_name, "attachment")
                    # dir_name = os.path.join(dir_name, year)
                    # dir_name = os.path.join(dir_name, month)
                    # dir_name = os.path.join(dir_name, date)
                    # serverimgpath1=self.readSql.read_config('attachmentPathReplace', '1')
                    # serverimgpath1=os.path.join(serverimgpath1,"attachment")
                    # serverimgpath1=os.path.join(serverimgpath1,year)
                    # serverimgpath1=os.path.join(serverimgpath1,month)
                    # serverimgpath1=os.path.join(serverimgpath1,date)
                    # if not os.path.exists(dir_name):
                    #     os.makedirs(dir_name)

                    if len(re.findall("rar", attachmenturl)) > 0:
                        attachmenturl_last=attachmenturl
                        # filename = os.path.join(dir_name, imguid + '.rar')
                        # serverimgpath1 = os.path.join(serverimgpath1,imguid + '.rar')
                    elif len(re.findall("pdf", attachmenturl)) > 0:
                        attachmenturl_last = attachmenturl
                        # filename = os.path.join(dir_name, imguid + '.pdf')
                        # serverimgpath1 = os.path.join(imguid + '.pdf')
                    elif len(re.findall("doc", attachmenturl)) > 0:
                        attachmenturl_last = attachmenturl
                        # filename = os.path.join(dir_name, imguid + '.doc')
                        # serverimgpath1 = os.path.join(imguid + '.doc')
                    elif len(re.findall("xls", attachmenturl)) > 0:
                        attachmenturl_last = attachmenturl
                        # filename = os.path.join(dir_name, imguid + '.xls')
                        # serverimgpath1 = os.path.join(imguid + '.xls')
                    elif len(re.findall("docx", attachmenturl)) > 0:
                        attachmenturl_last = attachmenturl
                        # filename = os.path.join(dir_name, imguid + '.docx')
                        # serverimgpath1 = os.path.join(imguid + '.docx')
                    elif len(re.findall("xlsx", attachmenturl)) > 0:
                        attachmenturl_last = attachmenturl
                        # filename = os.path.join(dir_name, imguid + '.xlsx')
                        # serverimgpath1 = os.path.join(imguid + '.xlsx')
                    elif len(re.findall("zip", attachmenturl)) > 0:
                        attachmenturl_last = attachmenturl
                        # filename = os.path.join(dir_name, imguid + '.zip')
                        # serverimgpath1 = os.path.join(imguid + '.zip')
                    else:
                        attachmenturl_last = ''
                    # opener = urllib.request.build_opener()
                    # opener.addheaders = [('User-Agent',
                    #                       'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36')]
                    # urllib.request.install_opener(opener)

                    try:
                        if attachmenturl_last!='':
                            #urllib.request.urlretrieve(attachmenturl, filename)
                            content_last = content_last.replace(src, attachmenturl_last)

                    except:
                        filename = "无效的附件路径"
                        print("无效的附件路径：" + attachmenturl)
                        #self.logger.info("无效的附件路径：%s", attachmenturl_last)
                    attachmentlist.append(attachmenturl_last)
                return content_last, str(attachmentlist)
        else:
            return content_last, str(attachmentlist)