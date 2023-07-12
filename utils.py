from config import *

async def mongo_insert_customer_impact(address, company_name, compensation):
    doc_shop = collection["customerImpact"].insert_one({
        'Address': address,
        'Company name': company_name,
        'Compensation': compensation
    })

    return True

async def mongo_insert_ishop_ipsos(address, company_name, compensation):
    doc_shop = collection["iShopIpsos"].insert_one({
        'Address': address,
        'Company name': company_name,
        'Compensation': compensation
    })

    return True

async def mongo_delete_customer_impact(address):
    doc_shop_delete = collection["customerImpact"].find_one(
        {'Address': address})

    return doc_shop_delete

async def mongo_delete_ishop_ipsos(address):
    doc_shop_delete = collection["iShopIpsos"].find_one(
        {'Address': address})

    return doc_shop_delete

# {'Address': 'Phillips 66-902 SOUNDVIEW PIT STOP INC, 902 SOUNDVIEW AVE, BRONX, NY, 10473, United States', 'Company name': 'Phillips 66', 'Compensation': 'Job Fee: $12.00\nExpenses: $10.00'}