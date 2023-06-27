from main import *

from fastapi_utils.tasks import repeat_every
from fastapi_utils.session import FastAPISessionMaker

from config import *

import requests
import schedule


@app.get("/")
# @app.on_event("startup")
# @repeat_every(seconds=20)
async def root():
    print("Root route initiated!")
    # url = "https://www.google.com/"
    url = 'http://127.0.0.1:5000/scraper/customerImpact'
    x = await requests.post(url)
    print("posted")
    print(x.text)
    return {"message": x.text}

@app.get("/heroku_test")
async def heroku_test():
    return {
        "Success": "Successful get request"
    }

#ADD A RECORD TO MONGODB
@app.post("/mongoDbPost")
async def mongo_db_post():
    doc_shop = collection.insert_one({
        "iShopIpsos": "False",
        "customerImpact": "False",
        "hsBrands": "False",
        "intelliShop": "False",
        "iSecretShop": "False",
    })

    return {
        "success": "Data entered successfully"
    }

#UPDATE MONGODB RECORD
@app.put("/mongoDbPut")
async def mongo_db_put():
    # doc_shop = collection.find(
    #     {"iShopIpsos": "False"}
    # )
    doc_shop_update = collection.find_one_and_update(
        {"iShopIpsos": "True"},
        {"$set": {"iShopIpsos": "False"}}
    )


    return {
        "success": "Data updated successfully"
    }