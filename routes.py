from main import *

from fastapi_utils.tasks import repeat_every
from fastapi_utils.session import FastAPISessionMaker

from config import *

import requests
import schedule


@app.get("/")
# @app.on_event("startup")
# @repeat_every(seconds=5)
async def root():
    print("Root route initiated!")
    url = "https://www.google.com/"
    # url = 'http://127.0.0.1:5000/scraper/test'
    x = requests.post(url)
    print("posted")
    print(x.status_code)
    return {"message": x.status_code}

@app.get("/heroku_test")
async def heroku_test():
    return {
        "Success": "Successful get request"
    }

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
