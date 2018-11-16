import re

class interception():
    def str_interception(self, body, jiequ_first, jiequ_last):
        try:
            interception_list_last=[]
            interception_list=body.split(jiequ_first)[1:]
            if len(interception_list) >= 1:
                for inter in interception_list:
                    if len(re.findall(jiequ_last, inter)) > 0:
                        inter_last=inter.split(jiequ_last)[0]
                        interception_list_last.append(inter_last)
                    else:
                        print('没有'+jiequ_last+'字符串')
            return interception_list_last
        except:
            print('没有截取到相关内容')

