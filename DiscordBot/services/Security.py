import json
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from discord.ext import commands

with open('databaseConfig.json') as f:
    data = json.load(f)
    connectionString = data["connection_string"]


class Security(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def findAll(self):
        client = MongoClient(connectionString, server_api=ServerApi('1'))
        mydb = client["StepSis"]
        mycol = mydb["Users"]
        for x in mycol.find({}, {"_id": 0, "user": 1}):
            print(x)

        client.close()


async def setup(client):
    await client.add_cog(Security(client))
