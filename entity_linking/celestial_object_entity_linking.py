import astroquery
from astroquery.simbad import Simbad
import argparse
import requests
import json
from helper import *

# path to the file where your ADS API token is stored
with open('ads_token_api', 'r') as file:
    ads_token = file.read().strip()

class CelestialObjectEntityLinking():

    def __init__(self, pipeline, source_name, KB, path_to_text, tokens, ner_tags):
        
        self.KB = KB
        self.pipeline = pipeline

        # if we only give a source name and simply want to get its unique identifier from a KB
        if self.pipeline == 'get_entity_identifier':
            self.source_name = source_name
        
        # if we already have NER predictions (list of tokens and their corresponding labels)
        elif self.pipeline == 'with_ner_preds':
            self.tokens = tokens
            self.ner_tags = ner_tags
            self.COb, self.source_name = extract_only_celestial_object_from_ner_module_output(self.tokens, self.ner_tags)


        # if we do not already have the NER predictions, we need to apply our NER model
        elif self.pipeline == 'do_ner_and_entity_linking':
            
            if path_to_text != None:
                with open(path_to_text, 'r') as text:
                    self.text = text.read()
                    self.tokens = self.text.split()
                    # we need to apply NER model for prediction
                    # self.pred_ner_tags = model.predict(self.tokens)
                    # self.COb, self.source_name = extract_only_celestial_object_from_ner_module_output(self.tokens, self.pred_ner_tags)

    def get_all_simbad_designations(self, source):
        # Connect to the SIMBAD database
        custom_simbad = Simbad()

        # Query SIMBAD for the astronomical source
        result_table = custom_simbad.query_objectids(source)

        if result_table is None:
            # Return an empty list if the source is not find in the catalogue
            return []
        
        else:
            # Return the list of all designations
            return result_table['ID'].tolist()
        
    def get_source_identifier_from_KB(self):

        if self.source_name == []:
            # if there is no Celestial Object in the document 
            print('No CelestialObject-type entity in the given list')
            return None
        
        else:

            payload = {"source": self.KB, "objects": self.source_name}

            results = requests.post("https://api.adsabs.harvard.edu/v1/objects", \
                                    headers = {"accept": "application/json", 
                                            "Authorization": "Bearer " + ads_token, 
                                            "content-type": "application/json"}, \
                                    data = json.dumps(payload))

            return results.json()
    
    def normalize_text(self):
        # Should we implement a method to normalize the text?
        # It can be further useful for the coreference resolution system to have some normalized entities? 
        return
    

def main():

    EL = CelestialObjectEntityLinking(pipeline, astrophysical_source_name, knowledge_base, path_to_text, tokens, ner_tags)
    results = EL.get_source_identifier_from_KB()
    print(results)
    return results

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description = 'This script is for CelestialObject-type entity linking.')

    # mandatory argument, to fix the usage mode of the implemented class
    parser.add_argument('--pipeline', required = True, type = str)

    # input arguments that will be used according the selected usage mode
    parser.add_argument('--source_name', required = False, type = str)
    parser.add_argument('--knowledge_base', required = False, type = str, default = 'SIMBAD')
    parser.add_argument('--path_to_text', required = False, type = float, default = None)
    parser.add_argument('--tokens', required = False, type = list, default = [])
    parser.add_argument('--ner_tags', required = False, type = list, default = [])

    args = parser.parse_args()
    pipeline = args.pipeline
    astrophysical_source_name = parse_input_source_name(args.source_name)
    knowledge_base = args.knowledge_base
    path_to_text = args.path_to_text
    tokens = args.tokens
    ner_tags = args.ner_tags

    results = main()





    
    




