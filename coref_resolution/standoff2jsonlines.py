import json
import glob
import gzip
import argparse
from utils import *

""" 

This script is useful if you want to use Fast-Coref for coreference resolution.
This script converts your corpus (from BRAT annotations format (.ann files)) into JSONLINES format for Fast-Coref.

"""

parser = argparse.ArgumentParser(description = 'This script is for converting BRAT annotations (.ann files) in .jsonlines format to use Fast-Coref model')
parser.add_argument('--corpus_dir', required = True, type = str)
args = parser.parse_args()
path_to_folder = args.corpus_dir



def standoff2jsonlines(path_to_folder, output_filename):

    ann_files = glob.glob(path_to_folder + '*.ann')

    list_of_dict = []

    for file in ann_files:

        filename = file.split(path_to_folder)[1].split('.ann')[0]

        with open(f'{path_to_folder}/{filename}.ann', 'r') as ann:
            ann = ann.read()

        with open(f'{path_to_folder}/{filename}.txt', 'r') as text:
            text = text.read()

        d = {}
        d['text'] = text

        unique_arg2 = []
        relations_info = []

        for row in ann.split('\n'):
                row = row.split('\t')
                if row != ['']:
                    if row[1].startswith('coreferring_to '):
                        link = row[1].split('coreferring_to ')
                        link = link[1]
                        relations_info.append(link)
                        arg1 = link.split('Arg1:')[1].split()[0]
                        arg2 = link.split('Arg2:')[1].split()[0]
                        if arg2 not in unique_arg2:
                            unique_arg2.append(arg2)

        clusters = []
        clusters_strings = []

        for entity_T in unique_arg2:
            
            mentions = []
            spans = []
            
            for r in relations_info:
                if r.endswith(f'Arg2:{entity_T}'):
                    arg1 = r.split()[0].split('Arg1:')[1]
                    for line in ann.split('\n'):
                        if line.startswith(f'{arg1}\t'):
                            m = line.split('\t')[-1] # get the mention
                            span_start, span_end = line.split('\t')[-2].split()[-2], line.split('\t')[-2].split()[-1] # get the spans (starting and ending) of the mention
                            spans.append([span_start, span_end])
                            mentions.append(m)
            
            for line in ann.split('\n'):
                if line.startswith(f'{entity_T}\t'):
                    mentions.append(line.split('\t')[-1])
                    span_start, span_end = line.split('\t')[-2].split()[-2], line.split('\t')[-2].split()[-1] # get the spans (starting and ending) of the mention
                    spans.append([span_start, span_end])


            clusters_strings.append(mentions)
            clusters.append(spans)
        
        d['clusters'] = clusters
        d['clusters_strings'] = clusters_strings

        list_of_dict.append(d)


    dicts_to_jsonl(list_of_dict, f'{output_filename}', False)


standoff2jsonlines(path_to_folder, 'TDAC_corpus')
