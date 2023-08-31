# Astrophysical Relation Extraction

Relation Extraction (RE) is a specific case of Information Extraction (IE) with the focus on the identification of semantic relations between entities (see Figure 1).

## Relation Types

We introduce five distinct relations that establish a systematic understanding of astrophysical entities. These relations are presented below and are classified into two conceptual categories: those about the spatial attributes of astrophysical objects and those linked to their intrinsic properties. By assigning the correct properties to their corresponding sources, even in cases where multiple sources are discussed within a text, we aim to enhance the information extraction process.

- `location_of`: Coordinates of an astrophysical object within the celestial sphere;
- `host_galaxy_of`: Connection between the astrophysical source and the galaxy in which it resides;
- `wavelength_of`: Wavelength associated with the emitted radiation from the source;
- `redshift_of`: The flux of a source, a measure of the energy passing through a unit area.

## Training a Relation Extraction System

### Data Format
