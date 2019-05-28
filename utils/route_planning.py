import requests, json
from datetime import datetime

### Constants ###
config = json.load(open('../config.json'))
BASE_URL = config["DISTANCE_MATRIX_BASE_URL"]
API_KEY = config["API_KEY"]

# Get the distance between two locations. Output response
# includes the distance in miles, and the time duration
# between the two locations.
#
#                     -- Parameters --
#    - origin: Address of the starting destination (STRING)
#    - destination: Address of the final destination (STRING)
#    - date_str: Date to use when calculating departure time.
#                Uses format "MM/DD/YYYY". (STRING)
#                Note: date_str is optional. Current datetime
#                      will be used if ommitted.
#    - time_str: Time to use when calculating departure time.
#                Uses format "HH:MM" (STRING)
#                Note: time_str is optional. Current datetime
#                      will be used if ommitted.
#
def get_distance(origin, destination, date_str=None, time_str=None):
	
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
		departure_dt = datetime(year, month, day, hour, minute, 0)
		departure_time = round((departure_dt - epoch).total_seconds())
	
	# Set parameters for API call
	params = {'units': 'imperial', \
				'origins': origin, \
				'destinations': destination, \
				'key': API_KEY, \
				'departure_time': departure_time}
	
	# Call the API to get the distance data
	r = requests.get(url=BASE_URL, params=params)
	return(r.json())
	

# Test call
print(get_distance('Durham, NC, USA', 'Raleigh, NC, USA'))