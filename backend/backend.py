import csv
from thefuzz import process, fuzz
import time
from urllib.parse import unquote
from flask import Flask, json, request, make_response
from flask_cors import CORS, cross_origin


# Rows in csv for rendering load progress on slower machines
TOTAL_LINES = 1628


def load(filename: str) -> dict[str, list[str]]:
    """Loads names and keywords from the provided csv.
    
    Loads names and keywords from the csv located at `filename` - keywords are augmented with names,
    industries, and locations to improve performance when identifying similar entries.
    """

    data = {}
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        print('Reading names...')
        index = 0
        for row in reader:
            # Display progress loading for slower machines
            completion = (index * 100 // TOTAL_LINES) // 2
            print("Loading: |{: <50}|".format('.' * completion), end='\r')

            # Append data plus augmented keywords
            data[row[2]] = row[2] + ', ' + row[3] + ', ' + row[9] + ', ' + row[-1]

            index += 1
    print("\nDone.")

    return data

def retrieve_profile(filename: str, target: str) -> list[str]:
        """Retrieves the full data for a given entry."""
        
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[2] == target:
                    return row

def search(term: str, data: list[str], min: int = 75) -> list[str]:
    """Finds the most relevant matches for a given company name.
    
    Searches through the loaded data for a given name and returns up to ten matches in order of
    confidence. A minimum confidence must be met - in the case that ten results do not meet this
    criteria less will be returned.

    Args:
        term (str): The search term
        data (list[str]): The names to be searched through
        min (int): The minimum confidence for a match to be considered. Defaults to 75(%)

    Returns:
        list[str]: A 0 <= N <= 10 list of matches.
    """

    # Find (max 10) closest matches to the given term
    found = process.extract(term, data, limit=10)

    relevant = []
    for x in found:
        if int(x[1]) >= min:
            # Only interested in matches with confidence greater than the provided minimum
            relevant.append(x)

    return [x[0] for x in relevant]

def find_similar(target: str, data: dict[str, list[str]], min: int = 70) -> list[str]:
    """Finds similar entries in the database.
    
    Finds up to ten entries in the database who's keywords are sufficiently close to the given
    target's. The minimum level of similarity to be considered a match can be specified. If more
    than 10 results match these criteria, only the 10 most confident are returned.

    Args:
        target (str): The name of the entry to be compared against
        data (dict[str, list[str]]): The other entries in the database, specifically their names and
                                     keywords.
        min (int): The minimum level of similarity required to e considered a relevant match.
                   Defaults to 70(%)
    
    Returns:
        list[str]: A list of names of similar entries
    """

    target_kwords = data[target]

    similarities = []
    for key in data.keys():
        # Find the similarity value for each entry in the database
        similarities.append([key, fuzz.token_set_ratio(target_kwords, data[key])])

    # Sort similarities in descending order
    similarities.sort(key=lambda x: x[1], reverse=True)
    # Remove the first value as it will always be the same as the target
    similarities = similarities[1:]

    close_enough = []
    while len(similarities) > 0 and len(close_enough) < 10 and similarities[0][1] >= min:
        # Select a maximum of ten other entries, and only those that meet the minimum similarity
        # value
        close_enough.append(similarities[0])
        similarities = similarities[1:]

    return close_enough


# Initial load of minimum data for searching
company_data = load('companies_data.csv')


## API ====================================================================== ##
# ============================================================================ #

# Initialize http server and basic CORS handling
api = Flask(__name__)
CORS(api)
# api.config['CORS_HEADERS'] = 'Content-Type'

@api.route('/api/retrieve', methods=['GET'])
def api_retrieve():
    """Endpoint for retrieving a specific entry in full detail"""

    api.logger.debug('retrieve')

    # Retrieve querystring arg and remove percent encoding
    company_name = unquote(request.args.get('name'))

    api.logger.debug('Attempting to retrieve full profile for {}'.format(company_name))
    data = retrieve_profile('companies_data.csv', company_name)
    api.logger.debug('Retrieved data')
    api.logger.info('Retrieved profile: {}'.format(data))

    return json.dumps(data)

@api.route('/api/search', methods=['GET', 'POST'])
# @cross_origin
def api_search():
    """Endpoint for searching for a string in entry names."""

    api.logger.debug('search')

    global company_data

    # Retrieve querystring arg and remove percent encoding
    company_name = unquote(request.args.get('name'))

    api.logger.debug('Searching for {}'.format(company_name))
    data = search(company_name, company_data.keys())
    api.logger.debug('Completed search')

    #debug#
    return json.dumps({'cont': 'words here'})

    return json.dumps(data)

@api.route('/api/similar', methods=['GET'])
def api_similar():
    """Endpoint for retrieving similar entries in database."""

    api.logger.debug('similar')

    global company_data

    # Retrieve querystring arg and remove percent encoding
    company_name = unquote(request.args.get('name'))

    results = find_similar(search(company_name, company_data.keys())[0], company_data, 70)
    return json.dumps([x[0] for x in results])

@api.route('/', methods=['GET'])
def test_up():
    return 'up'

# Start server listening on localhost:3068
if __name__ == '__main__':
    print("Starting server...")
    api.run(port=3068, debug=True)