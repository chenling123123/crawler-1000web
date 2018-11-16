import datetime
import re
import time
class filter():
    def date_clean(self,date):
        crawldate = datetime.datetime.now()
        if date and crawldate:
            date = date.replace(".", "-").replace("/", "-").replace("\n", "").replace("\\", "-")
            re_en = re.compile("(20[0-9][0-9]-\d{1,2}-\d{1,2}[\s])+\d{1,2}:\d{1,2}:\d{1,2}")
            re_en_s = re.compile("(18-\d{1,2}-\d{1,2}[\s])+\d{1,2}:\d{1,2}:\d{1,2}")
            re_cn = re.compile(u"(20[0-9][0-9]年\d{1,2}月\d{1,2}日[\s])+\d{1,2}时\d{1,2}分\d{1,2}秒")
            re_d_en = re.compile("(20[0-9][0-9]-(0[1-9]|1[0-2]|[1-9])-(0[1-9]|[12][0-9]|3[01]|[1-9]))")
            re_d_cn = re.compile(u"(20[0-9][0-9]年\d{1,2}月\d{1,2})日")
            re_n_cn = re.compile(u"(\d{2}年\d{1,2}月\d{1,2})日")
            re_m = re.compile("((0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01]|[1-9]))")
            re_d = re.compile(u"(昨天|前天|今天)")
            re_d_dn = re.compile(u"(\d{1,2})天前")
            re_d_mn = re.compile(u"(\d{1,2})月前")
            re_d_xn = re.compile(u"(\d{1,2})小时前")
            re_d_mmn = re.compile(u"(\d{1,2})分钟前")
            re_1 = re.compile("(20[0-9][0-9][0,1][0-9][0-3][0-9])")
            if re_en.search(str(date)):
                date = re_en.search(str(date)).group(1)
            elif re_en_s.search(str(date)):
                date = "20" + re_en.search(str(date)).group(1)
            elif re_cn.search(str(date)):
                date = re_cn.search(str(date)).group(1)
                date = date.replace("年", "-").replace("月", "-").replace("日", "")
            elif re_n_cn.search(str(date)):
                date = re_n_cn.search(str(date)).group(1)
                date = "20" + date.replace("年", "-").replace("月", "-").replace("日", "")
            elif re_d_en.search(str(date)):
                date = re_d_en.search(str(date)).group(1)
                date = date
            elif re_d_cn.search(str(date)):
                date = re_d_cn.search(str(date)).group(1)
                date = date.replace("年", "-").replace("月", "-").replace("日", "")
            elif re_m.search(str(date)):
                date = re_m.search(str(date)).group(1)
                date = "2018-" + date
            elif re_d.search(str(date)):

                if len(re.findall("今天", date)) > 0:

                    date = crawldate.strftime('%Y-%m-%d')
                elif len(re.findall("昨天", date)) > 0:
                    date = crawldate - datetime.timedelta(days=1)
                    date = date.strftime('%Y-%m-%d')
                elif len(re.findall("前天", date)) > 0:
                    date = crawldate - datetime.timedelta(days=2)
                    date = date.strftime('%Y-%m-%d')
            elif re_d_dn.search(str(date)):
                date = re_d_dn.search(str(date)).group(1)
                date = crawldate - datetime.timedelta(days=int(date))
                date = date.strftime('%Y-%m-%d')
            elif re_d_mn.search(str(date)):
                date = re_d_mn.search(str(date)).group(1)
                date = crawldate - datetime.timedelta(days=int(date) * 30)
                date = date.strftime('%Y-%m-%d')
            elif re_d_xn.search(str(date)):
                date = re_d_xn.search(str(date)).group(1)
                date = crawldate - datetime.timedelta(hours=int(date))
                date = date.strftime('%Y-%m-%d')
            elif re_d_mmn.search(str(date)):
                date = re_d_mmn.search(str(date)).group(1)
                date = crawldate - datetime.timedelta(minutes=int(date))
                date = date.strftime('%Y-%m-%d')
            elif re_1.search(str(date)):
                temp = re_1.search(str(date)).group(1)
                date = temp[0:4] + "-" + temp[4:6].zfill(2) + "-" + temp[6:8].zfill(2)
            else:
                date = ""

            return self.datecheck(date)

    def datecheck(self,date):
        if re.search("20[0-9][0-9]-\d{1,2}-\d{1,2}", date):
            date=date.split(" ")[0]
            pub_date=date[:10]
            return pub_date
        elif date[0]=='1':
            pub_date=int(date[0:10])
            timeArray = time.localtime(pub_date)
            otherStyleTime = time.strftime("%Y-%m-%d", timeArray)
            return otherStyleTime
        else:
            return ""

    def clean_mark(self,data):
        text = "".join(data)
        strlist = ['\\n', '\\r', '\\t', '&nbsp;', "\xa0", "\u3000", "\n", '\r', '\t', ')', ' ']
        for str in strlist:
            text = text.replace(str, '')
        return text
    def clean_mark_content(self,data):
        text = "".join(data)
        strlist = ['\\n', '\\r', '\\t', '&nbsp;', "\xa0", "\u3000", "\n", '\r', '\t', ' ']
        for str in strlist:
            text = text.replace(str, '')
        return text
    def contrast(self,date):
        try:
            crawldate = datetime.datetime.now()
            date=datetime.datetime.strptime(date, "%Y-%m-%d")
            return crawldate<date
        except Exception:
            raise Exception

    def delete_label(self,text):
        """:param li:保留的标签列表
        """
        lists = ['a', 'img', 'p', 'table', 'tr', 'td', 'font', 'br', 'div', 'style', 'script', 'b', 'strong', 'iframe',
                 'object', 'li', 'ul', 'dd', 'dt', 'sub', 'sup', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7',
                 'frame', 'form', 'span', 'hr', 'em', '!--', 'html', 'head', 'meta', 'title', 'input', 'center',
                 'section', 'tbody', 'voice', 'i', 'b', 'td','】','ucaptitle','th','P','PUBLISHTIME']

        for i in lists:
            str1 = '<' + i + '.*?' + '>'
            str2 = '</' + i + '>'
            reg = re.compile(str1)
            reg1 = re.compile(str2)
            text = reg.sub('', text)
            text = reg1.sub('', text)
        return text
