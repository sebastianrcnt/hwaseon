import asyncio
import datetime
import json
import glob
import os.path
from inspect import iscoroutinefunction
# cache-path


CACHE_FOLDER_PATH = 'data/'

def saveCache(cacheName: str, data: str):

  f = open(CACHE_FOLDER_PATH +
             f'{cacheName}|{datetime.datetime.now().isoformat()}.cache', 'w')
  f.write(data)
  f.close()

def checkCache(cacheName: str):
  # find all 
  return os.path.isfile(CACHE_FOLDER_PATH + cacheName + '|*.cache')
  


def applyCache(cacheName: str):
    def cache(apiFunc):
        if iscoroutinefunction(apiFunc):
            async def decoratedApiFunc(*args, **kwargs):
                res = await apiFunc(*args, **kwargs)
                saveCache(cacheName, json.dumps(res))
                return res
            return decoratedApiFunc
        else:
            def decoratedApiFunc(*args, **kwargs):
                res = apiFunc(*args, **kwargs)
                saveCache(cacheName, json.dumps(res))
                return res
            return decoratedApiFunc
    return cache


@applyCache('the api1')
async def api():
    await asyncio.sleep(1)
    return {'k': 1}


@applyCache('the api2')
def api2():
    return {'k2': 2}


# asyncio.run(api())
# api2()

# print(checkCache('the api1'))
print(glob.glob('data/*.cache'))
