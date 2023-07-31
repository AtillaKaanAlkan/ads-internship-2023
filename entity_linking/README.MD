Folder containing the entity linking pipeline and evaluation

# Get all designations of a celestial object with SIMBAD

In order to get all designations of an astrophysical object (let's say the most energetic GRB detected so far [GRB221009A](https://en.wikipedia.org/wiki/GRB_221009A)) using [SIMBAD](http://simbad.u-strasbg.fr/simbad/sim-basicIdent=m33&submit=SIMBAD+search) catalogue run the following command: `python request_simbad.py --source_name GRB221009A` . First, you may need to install the [Astroquery](https://astroquery.readthedocs.io/en/latest/) package (`pip install astroquery`).

The output will be a list with all the names of an astrophysical object. For instance, for GRB221009A, the output will be: 

`['SWIFT J1913.1+1946', 'GRB 221009A']`
