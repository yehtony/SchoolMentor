import json
import time
from typing import Dict, Any, List
import redis
from redis.commands.search.field import (
    NumericField,
    TagField,
    TextField,
    VectorField,
)
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import Query


def createClient() -> redis.Redis: 
    return redis.Redis(
        host="redis", 
        port=6379, 
        decode_responses=True
    )

def checkClient(client: redis.Redis) -> bool:
    return client.ping()

def updateDocuments(client: redis.Redis, keyValues: List[Dict[str, Any]], path:str="$") -> List[bool]:
    pipeline = client.pipeline()
    for data in keyValues:
        key: str = data['key']
        value: Dict[str, Any] = data['value']
        pipeline.json().set(key,path,value)
    return pipeline.execute()


# client = createClient()
# assert(checkClient(client))

def getByKey(client: redis.Redis, key: str) -> Dict[str, Any]:
    # return client.json().get("bikes:010", "$.model")
    return client.json().get(key)



# ## Insert
# mock_data: Dict[str, Any] = {
#     'model': 'ThrillCycle',
#     'brand': 'BikeShind',
#     'price': 815,
#     'type': 'Commuter Bikes',
#     'specs': {'material': 'alloy', 'weight': '12.7'},
#     'description': """ An artsy,  
#     retro-inspired bicycle that’s as functional as it is pretty: The ThrillCycle steel frame offers a smooth ride. 
#     A 9-speed drivetrain has enough gears for coasting in the city, but we wouldn’t suggest taking it to the mountains. 
#     Fenders protect you from mud, and a rear basket lets you transport groceries, flowers and books. 
#     The ThrillCycle comes with a limited lifetime warranty, so this little guy will last you long past graduation."""
# }

# res = updateDocuments(client,[{
#     'key': "bike:-1",
#     'value': mock_data
# }],"$")
# assert(all(res))
# # >>> [True, True, True, True, True, True, True, True, True, True, True]


# ## Search
# assert(getByKey(client, 'bike:-1')==mock_data)



# keys = sorted(client.keys("bikes:*"))
# print(f"client.keys(\"bikes:*\")): {keys}")
# # >>> ['bikes:001', 'bikes:002', ..., 'bikes:011']
