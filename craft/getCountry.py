import urllib.request as request
import json
import sys

def main(*argv):
	getData()
	parseData(*argv)

# Create data.json file
def getData():
	countryWithCode = {}
	# Call API
	with request.urlopen('https://www.travel-advisory.info/api') as response:
		if(response.getcode()==200):
			source = response.read()
			data = json.loads(source)
			for code in data['data'].keys():
				countryWithCode[code] = data['data'][code]['name']
			# Store the data into the file
			with open('data.json', 'w') as f:
				json.dump(countryWithCode, f, indent = 4, sort_keys = True)
		else:
			print('An error occurred while attempting to retrieve data from the API.')

def parseData(*argv):
	# Read data from the file
	with open('data.json') as f:
		data = json.load(f)
		for arg in argv[0]:
			getCountry(arg, data)

def getCountry(arg, data):
	# Convert all arguments to UpperCase
	arg = arg.upper()
	# Check whether country exists
	if arg in data:
		print(data[arg])
	else:
		print('Country not found.')

if __name__=='__main__':
    main(sys.argv[1:])