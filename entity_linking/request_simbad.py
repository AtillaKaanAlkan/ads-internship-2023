import astroquery
from astroquery.simbad import Simbad
import argparse

parser = argparse.ArgumentParser(description = 'This script is for obtaining all designations of an astrophysical objet using SIMBAD catalogue')
parser.add_argument('--source_name', required = True, type = str)
args = parser.parse_args()
source_name = args.source_name

def get_simbad_designations(source_name):
    # Connect to the SIMBAD database
    custom_simbad = Simbad()

    # Query SIMBAD for the astronomical source
    result_table = custom_simbad.query_objectids(source_name)

    if result_table is None:
        # Return an empty list if the source is not find in the catalogue
        return []
    
    else:
        # Return the list of all designations
        return result_table['ID'].tolist()

result_table = get_simbad_designations(source_name = source_name)
print(result_table)
