import bson
from bson import ObjectId
from models.model import BaseModel


class GreenHouseData(BaseModel):
    """GreenHouseData Model"""

    def __init__(self):
        super().__init__()
        return

    def insert(self, data: dict) -> dict:
        row = self.db.greenhousedata.insert_one(data)
        res = self.find(row.inserted_id)

        #TODO: Manera elegante de serializar?
        res["_id"] = str(res['_id'])
        res['user']['_id'] = str(res['user']['_id'])

        return res

    def find(self, id: ObjectId) -> dict:
        return self.db.greenhousedata.find_one({"_id": ObjectId(id)})

    def avg(self) -> dict:
        cursor = self.db.greenhousedata.aggregate([
            {
                '$group': {
                    '_id': '$user._id',
                    'avg_temp': {
                        '$avg': '$temp'
                    },
                    'avg_hum': {
                        '$avg': '$hum'
                    },
                    'avg_water_ph': {
                        '$avg': '$water_ph'
                    },
                    'avg_soil_ph': {
                        '$avg': '$soil_ph'
                    },
                    'avg_water_salinity': {
                        '$avg': '$water_salinity'
                    },
                    'avg_water_o2': {
                        '$avg': '$water_o2'
                    }
                }
            }, {
                '$addFields': {
                    'objectid': {
                        '$toObjectId': '$_id'
                    }
                }
            }, {
                '$lookup': {
                    'from': 'users',
                    'localField': 'objectid',
                    'foreignField': '_id',
                    'as': 'user',
                    'pipeline': [
                        {
                            '$project': {
                                'name': 1
                            }
                        }, {
                            '$addFields': {
                                '_id': {
                                    '$toString': '$_id'
                                }
                            }
                        }
                    ]
                }
            }, {
                '$unwind': {
                    'path': '$user'
                }
            }, {
                '$project': {
                    'objectid': 0,
                    '_id': 0
                }
            }
        ])

        return list(cursor)

    def history(self, user_id:str) -> []:

        filter = {
            'user._id': ObjectId(user_id)
        }
        sort = list({
                        'created': -1
                    }.items())

        cursor = self.db.greenhousedata.find(
            filter=filter,
            sort=sort
        )

        res = list()

        for data in cursor:
            data["_id"] = str(data['_id'])
            data['user']['_id'] = str(data['user']['_id'])
            res.append(data)

        return res

    def last(self, user_id:str) -> dict:

        filter = {
            'user._id': ObjectId(user_id)
        }
        sort = list({
                        'created': -1
                    }.items())

        data = self.db.greenhousedata.find_one(
            filter=filter,
            sort=sort
        )

        if data is not None:
            data["_id"] = str(data['_id'])
            data['user']['_id'] = str(data['user']['_id'])
            return data

        return None