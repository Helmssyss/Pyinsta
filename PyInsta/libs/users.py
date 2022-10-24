import aiosqlite
from typing import Tuple

class AllUsers:
    async def createTable(self):
        self.DATABASE = await aiosqlite.connect(database=r'users.sqlite')
        await self.DATABASE.execute("CREATE TABLE IF NOT EXISTS user_table (phpssid,mail,csrftoken,code,user_id)")
        await self.DATABASE.commit()