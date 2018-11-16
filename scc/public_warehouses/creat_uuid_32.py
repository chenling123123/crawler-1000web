import uuid

class uuid_32():
    def creat_uuid(self):
        id = uuid.uuid1()
        return str(id).replace("-","")
