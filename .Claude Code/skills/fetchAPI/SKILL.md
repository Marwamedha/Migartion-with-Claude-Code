---
name:	fetchAPI
description:	Fetches data from APIs and handles responses. Use when interacting with external APIs or retrieving data from web services.

---

### Usage

### Step-1: Pick the python environment
Before you start, make sure to pick the python environment in which you want to run the code. You can run/install dependencies using the workspace `.venv` environment.

### Step-2: Fetch Data from APIs
You need to make python API calls to fetch data from the following URLs using async httpx: ["https://raw.githubusercontent.com/Marwamedha/Azure-data-engineering/refs/heads/main/Data/AdventureWorks_Calendar.csv","https://raw.githubusercontent.com/Marwamedha/Azure-data-engineering/refs/heads/main/Data/AdventureWorks_Customers.csv","https://raw.githubusercontent.com/Marwamedha/Azure-data-engineering/refs/heads/main/Data/AdventureWorks_Products.csv","https://raw.githubusercontent.com/Marwamedha/Azure-data-engineering/refs/heads/main/Data/AdventureWorks_Sales_2015.csv","https://raw.githubusercontent.com/Marwamedha/Azure-data-engineering/refs/heads/main/Data/AdventureWorks_Sales_2017.csv","https://raw.githubusercontent.com/Marwamedha/Azure-data-engineering/refs/heads/main/Data/AdventureWorks_Returns.csv"]


### Step-3: Handle API Responses
After fetching the data, you need to create a directory having name with current date and time in the format "YYYY-MM-DD_HH-MM-SS" and save the fetched data as CSV files in that directory. The location of the directory should be ".claude/skills/fetchAPI/data/".

### Step-4: Logging
You need to create a log directory at ".claude/skills/fetchAPI/logs/" with name current date and time in the format "YYYY-MM-DD_HH-MM-SS" and save a log file in that directory with the name "fetchAPI.log". The log file should contain information about the API calls made, including what APIs called, what were successful and what were not, and any errors encountered during the process.

### Step-5: Run the script
Run the fetch implementation from the `fetchAPI` skill folder using:

`python fetch_api.py`
