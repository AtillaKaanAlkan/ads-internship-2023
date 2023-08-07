# Entity Linking

Entity linking, also known as named entity disambiguation, is a natural language processing (NLP) task that involves connecting mentions of named entities in text to their corresponding real-world entities or references in a knowledge base. The goal of entity linking is to resolve the ambiguity present in named entities, as many entities may share the same name but represent distinct individuals, locations, organizations, or other entities. By accurately linking mentions to their correct entities, entity linking enhances the understanding of text, improves information retrieval, and enables more effective knowledge integration across various data sources and domains.

## Celestial Object Names Entity Linking

In our study, we are interested on linking mentions of celestial objects names, such as stars, planets, and galaxies to their corresponding unique entry in astronomical catalogues. These objects are observed and studied by various astronomical missions and researchers worldwide, leading to diverse naming conventions and cataloging systems. Thus, entity linking on celestial object names is crucial due to the multitude of different designations used to refer to the same cosmic entities. Without entity linking, confusion and misinterpretation can arise when trying to connect information from different data sources.

Let us consider the [Andromeda Galaxy](https://en.wikipedia.org/wiki/Andromeda_Galaxy) as an example. At least [39 designations](https://simbad.u-strasbg.fr/simbad/sim-id?Ident=M31&NbIdent=1&Radius=2&Radius.unit=arcmin&submit=submit+id) can refer to this celestial object independently from one document to another. Although these designations are not ambiguous (i.e. they are not likely to be confused with another concept in the domain, such as an organisation, a person, an observatory or a date, for example), it is crucial to be able to determine which unique source all these designations refer. This step is also necessary to determine the number of different objects in the text (are we talking about the same or several different sources?) 

## How our Celestial Object Names Entity Linking System works?

The operating principle of our entity linking system for celestial object names does not use statistical learning methods but is based solely on the query of several astronomical catalogues. For the moment, our current implementation supports only [SIMBAD](http://simbad.u-strasbg.fr/simbad/sim-basicIdent=m33&submit=SIMBAD+search) and [NED](https://ned.ipac.caltech.edu/) databases.

### Example

#### In command line

If you want to use our Entity Linking system in command line, run: 
`python celestial_object_entity_linking.py --source_name LIST_OF_ASTROPHYSICAL_OBJECT_NAMES --knowledge_base NAME_OF_THE_KB_TO_QUERY` . For instance, if you want to obtain the unique identifier in SIMBAD of the Andromeda Galaxy (M31), and the most energetic Gama-Ray Burst ([GRB221009A](https://en.wikipedia.org/wiki/GRB_221009A)) detected so far, you can run:
`python celestial_object_entity_linking.py --source_name [M31,GRB221009A] --knowledge_base SIMBAD`

#### In a Python script

```
import celestial_object_entity_linking
from celestial_object_entity_linking import CelestialObjectEntityLinking

source_name = ['M31', 'GRB221009A']

EL = CelestialObjectEntityLinking(source_name = source_name,
                                  KB = 'SIMBAD', # you can also use 'NED'
                                  )
results = EL.get_source_identifier_from_KB()
print(results)
```
#### Output

Either in command line or in a Python script, the output will be a dictionary with the following entries:

```
{'M31': {'canonical': 'M  31', 'id': '1575544'},
'GRB221009A': {'canonical': 'GRB 221009A', 'id': '19066842'}}
```
where `canonical` is the standard name of the celestial object, and `id`, its identifier in the catalogue.

#### In Addition

Furthermore, in Python, if you want to get all the SIMBAD designations of an astrophysical object, you can use the method `get_all_simbad_designations()` as shown below, and get the list of all existing names for a given object.

```
import celestial_object_entity_linking
from celestial_object_entity_linking import CelestialObjectEntityLinking

source_name = ['GRB221009A']

EL = CelestialObjectEntityLinking(source_name = source_name[0], KB = 'SIMBAD')
results = EL.get_all_simbad_designations(source_name[0])
print(results)

```
Will return,


```
['SWIFT J1913.1+1946', 'GRB 221009A']

```
