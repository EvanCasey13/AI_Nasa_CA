import requests
import json
from time import sleep
import pprint
import os
from dotenv import load_dotenv
load_dotenv()
#Variables
api_key = os.getenv('API_KEY')
test_date="2024-10-20"

#Date range variables
start_date="2020-01-01"
end_date="2020-12-31"

def get_apod_data(api_key, date):
    if not api_key:
        print("API key not provided for request")
    elif not date:
        print("Date not provided, please add a date")
    else:
        try:
            request = requests.get(f'https://api.nasa.gov/planetary/apod?date={date}&api_key=' + api_key)
            response_data = request.json()
            #Format output
            response = {
                "date": response_data["date"],
                "title": response_data["title"],
                "url": response_data["url"],
                "explanation": response_data["explanation"],
                "media type": response_data["media_type"]
                }
            pprint.pprint(response)
            return response
        except ConnectionError as e:
            print(f"Network issues have prevented retrieval of data from the API, Error code:{e.errno}")
            

def fetch_multiple_apod_data(api_key, start_date, end_date):
    if not api_key:
        print("API key not provided for request")
    elif not start_date or not end_date:
        print("Date not provided, please add a date")
    else:
        try:
            request = requests.get(f'https://api.nasa.gov/planetary/apod?start_date={start_date}&end_date={end_date}&api_key=' + api_key)
            response_data = request.json()
            #check if file exists
            if os.path.exists("apod_data.json"):
                #if it does open the file in read mode and load the data into the dictionary
                 with open("apod_data.json", "r") as json_file:
                    try:
                        data = json.load(json_file)
                    #if an error occurs when loading the data reinitialise the dictionary    
                    except json.JSONDecodeError:
                        data = []
            #if it does not exist initialise empty dictionary
            else:
                data = []
                
            # Loop through all responses within date range
            for apod in response_data:
                response = get_apod_data(api_key=api_key, date=apod["date"])
                data.append(response)
                 
                #Open json file in write mode
                with open("apod_data.json", "w") as json_file:
                    json.dump(data, json_file, 
                        indent=4,  
                        separators=(',',': '))
                 
                # One second delay between loop iterations
                sleep(1)
                
        except ConnectionError as e:
            print(f"Network issues have prevented retrieval of data from the API")
        except PermissionError as e:    
            print(f"Permission denied: You do not have permission to alter this file")
        except IOError as e:
            print(f"An I/O error occurred when writing to this file. Error ID:{e.errno}, Description: {e.args}")
            
def read_apod_data():
    try:
        with open("apod_data.json", "r") as read_file:
            apod_data = json.load(read_file)
    except PermissionError as e:
        print(f"Permission denied: You do not have permission to read from this file. Error ID:{e.errno}")
        
    #Loop through and print data
    for apod in apod_data:
            print("Title: " + apod["title"] + " | " + "Date: " + apod["date"])
            
# Defining main function
def main():   
    #fetch_multiple_apod_data(api_key=api_key, start_date=start_date, end_date=end_date)
    read_apod_data()

if __name__=="__main__":
    main()