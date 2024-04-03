import csv
import time
from urllib.parse import unquote
from flask import Flask, json, request
from flask_cors import CORS

from db_util import create_client, insert_doc
from data_utils import *


MONGO_HOST = '172.17.0.2'
MONGO_PORT = 27017

# Connect to database
client = create_client('./companies_data.csv', MONGO_HOST, MONGO_PORT, False)

# Update database to contain all entries from the csv
with open('./companies_data.csv') as csvfile:
	csvreader = csv.reader(csvfile)
	headers = []
	content = []
	for row in csvreader:
		if headers == []:
			headers = row
			headers[0] = '_id'
		else:
			content.append(row)

for row in content:
	doc = {}
	for i in range(len(headers)):
		doc[headers[i]] = row[i]
	insert_doc(client.company_database.companies, doc, verbose=True)

# Initial load of minimum data for searching
company_data = load(client.company_database.companies)


## API ====================================================================== ##
# ============================================================================ #

# Initialize http server and basic CORS handling
api = Flask(__name__)
CORS(api)

@api.route('/api/retrieve', methods=['GET'])
def api_retrieve():
    """Endpoint for retrieving a specific entry in full detail"""

    # Retrieve querystring arg and remove percent encoding
    company_name = unquote(request.args.get('name'))

    api.logger.debug('Attempting to retrieve full profile for {}'.format(company_name))
    data = retrieve_profile(client.company_database.companies, company_name)
    api.logger.debug('Retrieved data')
    api.logger.info('Retrieved profile: {}'.format(data))

    return json.dumps(data)

@api.route('/api/search', methods=['GET'])
def api_search():
    """Endpoint for searching for a string in entry names."""

    global company_data

    # Retrieve querystring arg and remove percent encoding
    company_name = unquote(request.args.get('name'))

    api.logger.debug('Searching for {}'.format(company_name))
    data = search(company_name, company_data.keys())
    api.logger.debug('Completed search')

    return json.dumps(data)

@api.route('/api/similar', methods=['GET'])
def api_similar():
    """Endpoint for retrieving similar entries in database."""
    global company_data

    # Retrieve querystring arg and remove percent encoding
    company_name = unquote(request.args.get('name'))

    results = find_similar(search(company_name, company_data.keys())[0], company_data, 70)
    return json.dumps([x[0] for x in results])

# Start server listening on localhost:3068
if __name__ == '__main__':
    print("Starting server...")
    api.run(port=3068, debug=True)