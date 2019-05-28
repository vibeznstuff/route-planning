import requests, json
from datetime import datetime

### Constants ###
config = json.load(open('../config.json'))
BASE_URL = config["DISTANCE_MATRIX_BASE_URL"]
API_KEY = config["API_KEY"]

def get_distance(origin, destination, date_str, time_str):
	
	# Prepare the input information for departure_time
	# parameter.
	if date_str is None or time_str is None:
		departure_time = 'now'
	else:
		epoch = datetime.utcfromtimestamp(0)
		(month,day,year) = tuple([int(x) for x in date_str.split("/")])
		(hour,minute) = tuple([int(x) for x in time_str.split(":")])
		
		# Convert EST to UTC (Naive, change later to account for DST)
		if hour < 20:
			hour += 4
		else:
			hour = (hour + 4) - 24
			
		# Calculate the seconds since the epoch based on the entered
		# date and time value.
		departure_time = datetime(year, month, day, hour, minute, 0)
		dt_in_seconds = round((departure_time - epoch).total_seconds())
	
	# Set parameters for API call
	params = {'units': 'imperial', \
				'origins': origin, \
				'destinations': destination, \
				'key': API_KEY, \
				'departure_time': dt_in_seconds}
	
	# Call the API to get the distance data
	r = requests.get(url=BASE_URL, params=params)
	return(r.json())
	


# Test call
get_distance('Durham, NC, USA', 'Raleigh, NC, USA',"05/30/2019","17:00")