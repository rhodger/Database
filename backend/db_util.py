from pymongo import *
from pymongo.client_session import *
from pymongo.collection import Collection

def create_client(target_csv, mongo_host, mongo_port, reset_collection):
    client = MongoClient("mongodb://{}:{}/".format(mongo_host, mongo_port))
    print("Connected")
    
    if reset_collection:
        print('deleting companies collection..')
        client.company_database.drop_collection('companies')

    try:
        print('creating companies collection..')
        client.company_database.create_collection('companies', validator={
            '$jsonSchema': {
                'properties': {
                    '_id': {}, 
                    'linkedin_url': {},
                    'company_name': {}, 
                    'industry': {},
                    'website': {},
                    'tagline': {},
                    'about': {},
                    'year_founded': {},
                    'locality': {},
                    'country': {},
                    'current_employee_estimate': {},
                    'keywords': {}
                },
                'required': [
                    '_id', 'linkedin_url' , 'company_name', 'industry', 'website', 'tagline', 'about',
                    'year_founded', 'locality', 'country', 'current_employee_estimate', 'keywords'
                ],
                'additionalProperties': False,
            }
        })
    except Exception as e:
        print('failed to create companies collection: {}'.format(e))
    
    return client
		
def insert_doc(collection: Collection, document: dict, verbose: bool = True):
	if not collection.find_one(document):
		collection.insert_one(document)
	else:
		if verbose:
			print('failed to insert due to duplicate')