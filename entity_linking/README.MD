# Entity Linking

Entity linking, also known as named entity disambiguation, is a natural language processing (NLP) task that involves connecting mentions of named entities in text to their corresponding real-world entities or references in a knowledge base. The goal of entity linking is to resolve the ambiguity present in named entities, as many entities may share the same name but represent distinct individuals, locations, organizations, or other entities. By accurately linking mentions to their correct entities, entity linking enhances the understanding of text, improves information retrieval, and enables more effective knowledge integration across various data sources and domains.

## Celestial Object Names Entity Linking

In our study, we are interested on linking mentions of celestial objects names, such as stars, planets, and galaxies to their corresponding unique entry in astronomical catalogues. These objects are observed and studied by various astronomical missions and researchers worldwide, leading to diverse naming conventions and cataloging systems. Thus, entity linking on celestial object names is crucial due to the multitude of different designations used to refer to the same cosmic entities. Without entity linking, confusion and misinterpretation can arise when trying to connect information from different data sources.

Let us consider the Andromeda Galaxy as an example. At least [39 designations](https://simbad.u-strasbg.fr/simbad/sim-id?Ident=M31&NbIdent=1&Radius=2&Radius.unit=arcmin&submit=submit+id) can refer to this celestial object independently from one document to another. Although these designations are not ambiguous (i.e. they are not likely to be confused with another concept in the domain, such as an organisation, a person, an observatory or a date, for example), it is crucial to be able to determine which unique source all these designations refer. This step is also necessary to determine the number of different objects in the text (are we talking about the same or several different sources?) 

## How our Celestial Object Names Entity Linking System works?

The operating principle of our entity linking system for celestial object names does not use statistical learning methods but is based solely on the query of several astronomical catalogues. 

### Example

#### In command line

#### In a Python script







