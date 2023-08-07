from fastapi import Request, HTTPException
from datetime import datetime,time
import start_app
import connection
import check_json
from pydantic import BaseModel 
import json 
import pytz

app = connection.app

app.state.data_list = {}
app.state.data_list_next = {}
app.state.data_list_far = {}
app.state.data_list_far1 = {}
app.state.data_list_far2 = {}

#starting the fetch json data event
start_app.startup_event()

# Endpoint to serve the HTML template
@app.get("/")
async def get_table(request: Request):
    ist = pytz.timezone('Asia/Kolkata')
    current_time = datetime.now(ist).time()
    #current_time = datetime.now().time()
    start_time = time(9, 8)
    end_time = time(15, 33)
    if start_time <= current_time <= end_time:
        return connection.templates.TemplateResponse("oi_table.html", {"request": request})
    else:
        return connection.templates.TemplateResponse("market_closed.html", {"request": request})
    
oi_Data = []
oi_Data_next = []
oi_Data_far = []
oi_Data_far1 = []
oi_Data_far2 = []
# Endpoint to provide the updated table data
@app.get("/api/table-data")
async def get_table_data():
    ist = pytz.timezone('Asia/Kolkata')
    curr_time = datetime.now(ist).strftime("%d-%B-%Y %H:%M:%S")
    oi_Data.clear()
    oi_Data_next.clear()
    oi_Data_far.clear()
    oi_Data_far1.clear()
    oi_Data_far2.clear()
    try:
        option_chains = app.state.data_list.get("optionChains", [])
        option_chains_next = app.state.data_list_next.get("optionChains", [])
        option_chains_far = app.state.data_list_far.get("optionChains", [])
        option_chains_far1 = app.state.data_list_far1.get("optionChains", [])
        option_chains_far2 = app.state.data_list_far2.get("optionChains", [])
        for option_chain in option_chains:
            ce_open_interest = option_chain["callOption"]["openInterest"]
            pe_open_interest = option_chain["putOption"]["openInterest"]
            ce_volume = option_chain["callOption"]["volume"]
            pe_volume = option_chain["putOption"]["volume"]
            oi_Data.append({"strikePrice": option_chain["strikePrice"], "ce_openInterest": ce_open_interest, "pe_openInterest": pe_open_interest, "ce_volume": ce_volume,"pe_volume": pe_volume})

        for option_chain_next in option_chains_next:
            ce_open_interest_next = option_chain_next["callOption"]["openInterest"]
            pe_open_interest_next = option_chain_next["putOption"]["openInterest"]
            ce_volume_next = option_chain_next["callOption"]["volume"]
            pe_volume_next = option_chain_next["putOption"]["volume"]
            oi_Data_next.append({"strikePrice": option_chain_next["strikePrice"], "ce_openInterest": ce_open_interest_next, "pe_openInterest": pe_open_interest_next, "ce_volume": ce_volume_next,"pe_volume": pe_volume_next})

        for option_chain_far in option_chains_far:
            ce_open_interest_far = option_chain_far["callOption"]["openInterest"]
            pe_open_interest_far = option_chain_far["putOption"]["openInterest"]
            ce_volume_far = option_chain_far["callOption"]["volume"]
            pe_volume_far = option_chain_far["putOption"]["volume"]
            oi_Data_far.append({"strikePrice": option_chain_far["strikePrice"], "ce_openInterest": ce_open_interest_far, "pe_openInterest": pe_open_interest_far, "ce_volume": ce_volume_far,"pe_volume": pe_volume_far})
        
        for option_chain_far1 in option_chains_far1:
            ce_open_interest_far1 = option_chain_far1["callOption"]["openInterest"]
            pe_open_interest_far1 = option_chain_far1["putOption"]["openInterest"]
            ce_volume_far1 = option_chain_far1["callOption"]["volume"]
            pe_volume_far1 = option_chain_far1["putOption"]["volume"]
            oi_Data_far1.append({"strikePrice": option_chain_far1["strikePrice"], "ce_openInterest": ce_open_interest_far1, "pe_openInterest": pe_open_interest_far1, "ce_volume": ce_volume_far1,"pe_volume": pe_volume_far1})
        
        for option_chain_far2 in option_chains_far2:
            ce_open_interest_far2 = option_chain_far2["callOption"]["openInterest"]
            pe_open_interest_far2 = option_chain_far2["putOption"]["openInterest"]
            ce_volume_far2 = option_chain_far2["callOption"]["volume"]
            pe_volume_far2 = option_chain_far2["putOption"]["volume"]
            oi_Data_far2.append({"strikePrice": option_chain_far2["strikePrice"], "ce_openInterest": ce_open_interest_far2, "pe_openInterest": pe_open_interest_far2, "ce_volume": ce_volume_far2,"pe_volume": pe_volume_far2})

    except KeyError as e:
        print(f"Error accessing optionChains: {str(e)}")
    return {"oi_data": oi_Data,"oi_data_next":oi_Data_next,"oi_data_far":oi_Data_far,"oi_data_far1":oi_Data_far1,"oi_data_far2":oi_Data_far2, "curr_time": curr_time}

# Global variable to store oi_PCR_avg values
oi_pcr_avg_data = []

# Pydantic model for receiving oi_PCR_avg value from frontend
class OIPCRAvgData(BaseModel):
    curr_time: str
    oi_pcr_avg: float

@app.post("/api/save-oi-pcr-avg")
async def save_oi_pcr_avg(data: OIPCRAvgData):

    # Input date and time string
    input_datetime_str = data.curr_time
    # Define the format of the input date and time string
    input_format = "%d-%B-%Y %H:%M:%S"
    # Convert the input string to a datetime object
    dt_obj = datetime.strptime(input_datetime_str, input_format)
    # Extract hours, minutes, and seconds from the datetime object
    hours = dt_obj.hour
    minutes = dt_obj.minute
    seconds = dt_obj.second
    # Format the output as hh:mm:ss
    output_time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    data.curr_time = output_time_str

    try:
        # Save oi_PCR_avg and current time values to the global variable
        oi_pcr_avg_data.append({"curr_time": data.curr_time, "oi_pcr_avg": data.oi_pcr_avg})
        # Save oi_pcr_avg_data to a JSON file (modify the file path as needed)
        with open("oi_pcr_avg_data.json", 'w') as file:
            json.dump(oi_pcr_avg_data, file)
            
        return {print("oi_PCR_avg and current time values saved successfully.")}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error saving oi_PCR_avg and current time values.")
