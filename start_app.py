import connection
import fetch 
import asyncio
from datetime import datetime,time
import pytz

app = connection.app 

# Start the background task to update the live data
@app.on_event("startup")
async def startup_event():
    ist = pytz.timezone('Asia/Kolkata')
    current_time = datetime.now(ist).time()
    #current_time = datetime.now().time()
    start_time = time(9, 8)
    end_time = time(15, 33)
    if start_time <= current_time <= end_time:
        url = "https://groww.in/v1/api/option_chain_service/v1/option_chain/nifty?expiry=2023-08-10"  # Replace this URL with the data source URL
        url_next = "https://groww.in/v1/api/option_chain_service/v1/option_chain/nifty?expiry=2023-08-17"
        url_far = "https://groww.in/v1/api/option_chain_service/v1/option_chain/nifty?expiry=2023-08-31"
        url_far1 = "https://groww.in/v1/api/option_chain_service/v1/option_chain/nifty?expiry=2023-09-28"
        url_far2 = "https://groww.in/v1/api/option_chain_service/v1/option_chain/nifty?expiry=2023-12-28"
        filename = "dw_data.json"  # Choose the desired filename for the saved data
        filename_next = "dw_data_next.json"
        filename_far = "dw_data_far.json"
        filename_far1 = "dw_data_far1.json"
        filename_far2 = "dw_data_far2.json"
        asyncio.create_task(fetch.fetch_and_save_data(url, filename))
        asyncio.create_task(fetch.fetch_and_save_data_next(url_next, filename_next))
        asyncio.create_task(fetch.fetch_and_save_data_far(url_far, filename_far))
        asyncio.create_task(fetch.fetch_and_save_data_far1(url_far1, filename_far1))
        asyncio.create_task(fetch.fetch_and_save_data_far2(url_far2, filename_far2))
    else: 
        print ("Market closed !")

