import json
import gzip

def dicts_to_jsonl(data_list: list, filename: str, compress: bool = True) -> None:
    """
    Method saves list of dicts into jsonlines file.

    :param data: (list) list of dicts to be stored,
    :param filename: (str) path to the output file. If suffix .jsonlines is not given then methods appends
        .jsonlines suffix into the file.
    :param compress: (bool) should file be compressed into a gzip archive?
    """

    sjsonl = '.jsonlines'
    sgz = '.gz'

    # Check filename

    if not filename.endswith(sjsonl):
        filename = filename + sjsonl

    # Save data
    
    if compress:
        filename = filename + sgz
        with gzip.open(filename, 'w') as compressed:
            for ddict in data_list:
                jout = json.dumps(ddict) + '\n'
                jout = jout.encode('utf-8')
                compressed.write(jout)
    else:
        with open(filename, 'w') as out:
            for ddict in data_list:
                jout = json.dumps(ddict) + '\n'
                out.write(jout)