from flask import Flask
import urllib.request as request
import requests
import json
import sys
from http import HTTPStatus
from healthcheck import HealthCheck, EnvironmentDump

app = Flask(__name__)

health = HealthCheck()
envdump = EnvironmentDump()

# return health of the service
def convertCountry_available():
	client = convert('Australia')
	return True, "convert() ok"
health.add_check(convertCountry_available)
# Add a flask route to expose information
app.add_url_rule("/health", "healthcheck", view_func=lambda: health.run())

@app.route('/')
def get_country_code():
    return 'Get Country Code'

# Status of the api https://www.travel-advisory.info/api
@app.route('/diag')
def callURL():
	response = requests.get('https://www.travel-advisory.info/api')
	if(response.status_code==200):
		return response.reason
	return 'An error occurred while attempting to retrieve data from the API.'

# Converts country name to country code
@app.route('/convert/<code>')
def convert(code):
	getData()
	result = parseData(code)
	print(result)
	if(result):
		return result
	return 'Please check the error.'
	# parseData(code)

# Create data.json file
def getData():
	countryWithCode = {}
	# Call API
	with request.urlopen('https://www.travel-advisory.info/api') as response:
		if(response.getcode()==200):
			source = response.read()
			data = json.loads(source)
			for code in data['data'].keys():
				countryName = data['data'][code]['name']
				countryWithCode[countryName] = code
			# Store the data into the file
			with open('data.json', 'w') as f:
				json.dump(countryWithCode, f, indent = 4, sort_keys = True)
		else:
			print('An error occurred while attempting to retrieve data from the API.')

def parseData(argv):
	# Read data from the file
	# print(argv)
	with open('data.json') as f:
		data = json.load(f)
		result = getCountry(argv, data)
	return result

def getCountry(argv, data):
	print(argv)
	# Check whether country exists
	if argv in data:
		result = data[argv]
	else:
		result = 'Country Code not found.'
	return result

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')