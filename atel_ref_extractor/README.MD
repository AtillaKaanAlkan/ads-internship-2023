# Extract references and other useful information from ATels (astronomical telegrams) and GCN Circulars

### The Astronomers' Telegram (ATel)

The Astronomer's Telegram publication system (ATel) is a communication channel enabling to share and report astronomical discoveries for the benefit of the whole professional astrophysicists' community. The ATel system overcomes this challenge by making available observation reports (the so-called "telegrams") posted by observers on the web portal instantaneously. Therefore, this system provides verifiable information while minimising the distribution time and maximising the availability of posted telegrams. All reports are free to access and free to use.

### The GCN Network (GCN)

The GCN platform is dedicated mainly to the gamma-ray bursts astrophysicists community, where observers report their observations and analysis of GRBs in the form of "GCN Circulars".


### Extracting Metadata (including References) from ATels and GCN circulars

#### Principle of the Script
This script enables to extract a given ATel or GCN circular and all information (metadata) related to it: title, subject, publication date, authors, fulltext, and all references to other observations reports.

#### Example of a Use-case: Extracting references and metadata from ATel No. 16116
Assume you want to scrap the latest ATel (let's say ATel No. 16116) from the website. In order to extract its metadata, run the following command: `python report_scraper.py --report_type atel --report_id 16116`. Then, the script will return a dictionary with the following entries:

```
{'report_id': 16116,

 'authors': ['Andrew Hughes (U. Alberta), Thomas Russell (INAF-IASF Palermo), Rob Fender (Oxford),
              Patrick Woudt (U. Cape Town), James Miller-Jones (Curtin), on behalf of the 
              ThunderKAT collaboration'],

 'fulltext':,

 'fulltext_references_links': ['https://www.astronomerstelegram.org/?read=16097',
                               'https://www.astronomerstelegram.org/?read=16100',
                               'https://www.astronomerstelegram.org/?read=16102'],
 
 'fulltext_references_regexp': [('ATel #16097', (188, 199)),
                                ('ATel #16100', (403, 414)),
                                ('ATel #16102', (533, 544)],

 'related_references_links': ['https://www.astronomerstelegram.org/?read=16124',
                              'https://www.astronomerstelegram.org/?read=16116',
                              'https://www.astronomerstelegram.org/?read=16108',
                              'https://www.astronomerstelegram.org/?read=16105',
                              'https://www.astronomerstelegram.org/?read=16102',
                              'https://www.astronomerstelegram.org/?read=16100',
                              'https://www.astronomerstelegram.org/?read=16097',
                              'https://www.astronomerstelegram.org/?read=11869',
                              'https://www.astronomerstelegram.org/?read=10137',
                              'https://www.astronomerstelegram.org/?read=9541',
                              'https://www.astronomerstelegram.org/?read=9517',
                              'https://www.astronomerstelegram.org/?read=5991',
                              'https://www.astronomerstelegram.org/?read=5986'],

  'subjects': 'Radio, X-ray, Black Hole, Transient',

  'title': 'ATel #16116: MeerKAT radio detection of GRS 1739-278 during its '
             'recent outburst'

}
```


