from main import *
from config import *
from ultraMessage import *

from fastapi_utils.tasks import repeat_every
from fastapi_utils.session import FastAPISessionMaker

import httpx
import asyncio
import schedule

URL_CUSTOMER_IMPACT = 'http://127.0.0.1:5000/scraper/customerImpact'
URL_ISHOP_IPSOS = 'http://127.0.0.1:5000/scraper/iShopIpsos'

URL_PROD_CUSTOMER_IMPACT = 'http://mysteryshops.pythonanywhere.com/scraper/customerImpact'
URL_PROD_ISHOP_IPSOS = 'http://mysteryshops.pythonanywhere.com/scraper/iShopIpsos'

# async def task():
#     async with httpx.AsyncClient() as client:
#         resp = await client.get(URL)
#         shops = resp.text
#         return shops

CUSTOMER_IMPACT_FLAG = False
ISHOP_IPSOS_FLAG = False

@app.get("/")
async def root():
    return {"result": "Success"}

@app.get("/customer_impact")
@app.on_event("startup")
@repeat_every(seconds=180)
async def customer_impact():
    if not CUSTOMER_IMPACT_FLAG:
        print("Root route initiated!")
        CUSTOMER_IMPACT_FLAG = True
        async with httpx.AsyncClient() as client:
            resp = await client.get(URL_PROD_CUSTOMER_IMPACT, timeout=None)
            # resp = await client.get(URL_PROD, timeout=None)
            send_message("+923352839515", "-----------Customer Impact Alert-----------")
            all_jobs = resp.json()["Customer Impact Jobs"]
            print(all_jobs)
            job_string = ""
            for k,v in all_jobs.items():
                job_string += f"Address: {k} Company name: {v['Company name']} Compensation: {v['Compensation']}\n"
                print(job_string)
            send_message("+923352839515", job_string)

        return {"result": "Success"}
    return {"result": "Worker busy"}

@app.get("/ishop_ipsos")
@app.on_event("startup")
@repeat_every(seconds=160)
async def ishop_ipsos():
    if not ISHOP_IPSOS_FLAG:
        print("Root route initiated!")
        ISHOP_IPSOS_FLAG = True
        async with httpx.AsyncClient() as client:
            resp = await client.get(URL_PROD_ISHOP_IPSOS, timeout=None)
            # resp = await client.get(URL_PROD, timeout=None)
            send_message("+923352839515", "-----------Ishop Ipsos Alert-----------")
            all_jobs = resp.json()["IShop Ipsos Jobs"]
            print(all_jobs)
            job_string = ""
            for k,v in all_jobs.items():
                job_string += f"Address: {k} Company name: {v['Company name']} Compensation: {v['Compensation']}\n"
            send_message("+923352839515", job_string)

        return {"result": "Success"}
    return {"result": "Worker busy"}


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