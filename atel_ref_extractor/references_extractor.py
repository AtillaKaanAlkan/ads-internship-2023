import re

def extract_references_with_regular_expressions(text):

    
    regex_patterns = [
        # for GCN circulars
        r'GCN\s\d+',

        # for ATels
        r'ATel\s#\d+',
        r'ATel#\d+',
        r'Atel#\d+',
        r'Atel\s#\d+',
        
        r'ATEL\s#\d+',
        r'ATEL#\d+',


        r'ATels\s#\d+',
        r"ATels\s#(\d+(?:,\s#\d+)*)",
        r"ATel\s#(\d+(?:,\s#\d+)*)",
        r"ATel\s#(\d+(?:;\s#\d+)*)",


        # for CBAT (frequently used?)
        r'CBET\s\d+'


        
    ]

    identified_expressions = []

    for pattern in regex_patterns:
        
        matches = re.finditer(pattern, text)
        
        for match in matches:
            
            expression = match.group()
            span = match.span()
            identified_expressions.append((expression, span))

    return identified_expressions

# Test with an example
#path = '/home/alkan/Documents/NLP/BRAT/brat-1.3p1/data/astrophysics/TDAC/preannotated_TDAC75_V2/'
path = '/home/alkan/Documents/NASA-ADS/Internship/'
with open(path + 'example_atel', 'r') as f:
    f = f.read()

results = extract_references_with_regular_expressions(f)

for expression, span in results:
    print(f"Expression: '{expression}' - Span: {span}")
