from main import *
from config import *
from utils import *
from ultraMessage import *

from fastapi_utils.session import FastAPISessionMaker
from fastapi_utils.tasks import repeat_every

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

WORKER_STACK = ["iShopIpsos","customerImpact"]
WORKER_THREAD = False

@app.on_event("startup")
@repeat_every(seconds=30)
@app.get("/")
async def root():
    if not WORKER_THREAD:
        print("Here")
        print(WORKER_STACK)
        print(WORKER_THREAD)
        if WORKER_STACK[0] == "customerImpact":
            print("Here")
            obj = await customer_impact()
            # asyncio.run(obj)
        elif WORKER_STACK[0] == "iShopIpsos":
            obj = await ishop_ipsos()
            # asyncio.run(obj)
        return {"status": "Success"}
    else:
        print("Worker busy ya'll")
        return {"status": "Worker busy"}


async def customer_impact():
    print("Root route initiated!")
    WORKER_THREAD = True
    async with httpx.AsyncClient() as client:
        resp = await client.get(URL_PROD_CUSTOMER_IMPACT, timeout=None)
        # resp = await client.get(URL_CUSTOMER_IMPACT, timeout=None)
        send_message("+923352839515", "-----------Customer Impact Alert-----------")
        all_jobs = resp.json()["Customer Impact Jobs"]
        print(all_jobs)
        job_string = ""
        for k,v in all_jobs.items():
            job_check = await mongo_delete_customer_impact(k)
            print(job_check)
            if not job_check:
                job_insert = await mongo_insert_customer_impact(k, v['Company name'], v['Compensation'])
                job_string += f"Address: {k} Company name: {v['Company name']} Compensation: {v['Compensation']}\n\n"
        print(job_string)
        send_message("+923352839515", job_string)

    popped = WORKER_STACK.pop(0)
    WORKER_STACK.append(popped)
    WORKER_THREAD = False

    return {"result": "Success"}


async def ishop_ipsos():
    print("Root route initiated!")
    WORKER_THREAD = True
    async with httpx.AsyncClient() as client:
        resp = await client.get(URL_PROD_ISHOP_IPSOS, timeout=None)
        # resp = await client.get(URL_ISHOP_IPSOS, timeout=None)
        send_message("+923352839515", "-----------Ishop Ipsos Alert-----------")
        all_jobs = resp.json()["IShop Ipsos Jobs"]
        print(all_jobs)
        job_string = ""
        for k,v in all_jobs.items():
            job_check = await mongo_delete_ishop_ipsos(k)
            print(job_check)
            if not job_check:
                job_insert = await mongo_insert_ishop_ipsos(k, v['Company name'], v['Compensation'])
                job_string += f"Address: {k} Company name: {v['Company name']} Compensation: {v['Compensation']}\n"
        print(job_string)
        send_message("+923352839515", job_string)

    popped = WORKER_STACK.pop(0)
    WORKER_STACK.append(popped)
    WORKER_THREAD = False

    return {"result": "Success"}


#ADD A RECORD TO MONGODB
@app.post("/mongoDbPost")
async def mongo_db_post():
    doc_shop = collection["iShopIpsos"].insert_one({
        'Address': 'Phillips 66-902 SOUNDVIEW PIT STOP INC, 902 SOUNDVIEW AVE, BRONX, NY, 10473, United States', 'Company name': 'Phillips 66', 'Compensation': 'Job Fee: $12.00\nExpenses: $10.00'
    })

    return {
        "success": "Data entered successfully"
    }

#UPDATE MONGODB RECORD
@app.post("/mongoDbPut")
async def mongo_db_put():
    # doc_shop = collection.find(
    #     {"iShopIpsos": "False"}
    # )
    doc_shop_update = collection["iShopIpsos"].find_one_and_delete({'Address':'Phillips 66-902 SOUNDVIEW PIT STOP INC, 902 SOUNDVIEW AVE, BRONX, NY, 10473, United States'})
    print(doc_shop_update)

    return {
        "success": "Data updated successfully"
    }