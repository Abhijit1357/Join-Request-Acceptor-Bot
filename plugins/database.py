import motor.motor_asyncio
from config import DB_NAME, DB_URI

class Database:
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users
        self.settings = self.db.settings

    def new_user(self, id, name):
        return dict(
            id = id,
            name = name,
            session = None,
        )

    async def add_user(self, id, name):
        user = self.new_user(id, name)
        await self.col.insert_one(user)

    async def is_user_exist(self, id):
        user = await self.col.find_one({'id':int(id)})
        return bool(user)

    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count

    async def get_all_users(self):
        return self.col.find({})

    async def delete_user(self, user_id):
        await self.col.delete_many({'id': int(user_id)})

    async def set_session(self, id, session):
        await self.col.update_one({'id': int(id)}, {'$set': {'session': session}})

    async def get_session(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user['session']

    async def set_time(self, time):
        await self.settings.update_one({}, {'$set': {'time': time}}, upsert=True)

    async def get_time(self):
        settings = await self.settings.find_one({})
        return settings['time']

    async def set_channel(self, channel_id):
        await self.settings.update_one({}, {'$set': {'channel_id': channel_id}}, upsert=True)

    async def get_channel(self):
        settings = await self.settings.find_one({})
        return settings['channel_id']

db = Database(DB_URI, DB_NAME)
