import astroquery
from astroquery.simbad import Simbad
import argparse
import requests
from urllib.parse import urlencode, quote_plus
import json

parser = argparse.ArgumentParser(description = 'This script is for obtaining all designations of an astrophysical objet using SIMBAD catalogue')
parser.add_argument('--source_name', required = True, type = str)
parser.add_argument('--knowledge_base', required = False, type = str, default = 'SIMBAD')

args = parser.parse_args()

astrophysical_source_name = args.source_name
knowledge_base = args.knowledge_base

ads_token = '5oBPxwudqJQLT6JBH0ovGeD34eC8ECy6Eg9UqzQ6'

class EntityLinking():

    def __init__(self, source_name, KB):

        self.source_name = source_name
        self.KB = KB
  
    def get_all_simbad_designations(self):
        # Connect to the SIMBAD database
        custom_simbad = Simbad()

        # Query SIMBAD for the astronomical source
        result_table = custom_simbad.query_objectids(self.source_name)

        if result_table is None:
            # Return an empty list if the source is not find in the catalogue
            return []
        
        else:
            # Return the list of all designations
            return result_table['ID'].tolist()
        
    def get_identifiers_from_KB(self):

        payload = {"source": self.KB, "objects": [self.source_name]}

        results = requests.post("https://api.adsabs.harvard.edu/v1/objects", \
                                headers = {"accept": "application/json", 
                                            "Authorization": "Bearer " + ads_token, 
                                            "content-type": "application/json"}, \
                                data = json.dumps(payload))

        return results.json()



EL = EntityLinking(astrophysical_source_name, knowledge_base)
results = EL.get_identifiers_from_KB()
print(results)
