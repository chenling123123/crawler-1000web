import datetime
class pickTime():
    def creat_pick_time(self):
        pickTime = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return pickTime
