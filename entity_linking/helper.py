import seqeval
from seqeval.metrics.sequence_labeling import *

def extract_only_celestial_object_from_ner_module_output(tokens, tags):
    
    Cob_only = [elem for elem in get_entities(tags) if elem[0] == 'CelestialObject']
    
    sources_names = []

    for cob in Cob_only:
        sources_names.append(" ".join(w for w in tokens[cob[1]: cob[-1]]))
    
    return Cob_only, sources_names

def parse_input_source_name(list_of_source_name):

    parsed_source_name = list_of_source_name[1:-1].split(',')

    return parsed_source_name

