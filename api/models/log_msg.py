import bson
from bson import ObjectId
from models.model import BaseModel


class LogMsg(BaseModel):
    """LogMsg Model"""

    def __init__(self):
        super().__init__()
        return

    def insert(self, data: dict) -> dict:

        if data["user"] is not None:
            data["user"]["_id"] = ObjectId(data["user"]["_id"])

        row = self.db.logmsg.insert_one(data)

        return row

    def find(self, id: ObjectId) -> dict:
        return self.db.logmsg.find_one({"_id": ObjectId(id)})


    def history(self) -> []:

        filter = {}
        sort = list({
                        'created': -1
                    }.items())

        cursor = self.db.logmsg.find(
            filter=filter,
            sort=sort
        )

        res = list()

        for data in cursor:
            data["_id"] = str(data['_id'])

            if data["user"] is not None:
                data['user']['_id'] = str(data['user']['_id'])

            res.append(data)

        return res